"""
FLUID STRATOS - A Teljes Újragondolás
"""

import numpy as np
import jax.numpy as jnp
from jax import jit
import matplotlib.pyplot as plt

class FluidSTRATOS:
    """
    STRATOS újragondolva folyékony rendszerként
    
    NEM komponensek gyűjteménye
    HANEM egyetlen kognitív mező különböző mintázatokkal
    """
    
    def __init__(self, 
                 grid_size=(128, 128),  # 2D mező (gazdagabb!)
                 domain_size=20.0,
                 n_modes=16):
        
        # ═══ A MEZŐ ═══
        self.Nx, self.Ny = grid_size
        self.L = domain_size
        self.dx = domain_size / grid_size[0]
        
        # 2D térháló
        x = np.linspace(-self.L/2, self.L/2, self.Nx)
        y = np.linspace(-self.L/2, self.L/2, self.Ny)
        self.X, self.Y = np.meshgrid(x, y)
        
        # Impulzus tér (FFT-hez)
        kx = 2*np.pi*np.fft.fftfreq(self.Nx, self.dx)
        ky = 2*np.pi*np.fft.fftfreq(self.Ny, self.dx)
        self.KX, self.KY = np.meshgrid(kx, ky)
        self.K2 = self.KX**2 + self.KY**2
        
        # KOGNITÍV HULLÁMFÜGGVÉNY
        self.ψ = self._initialize_field()
        
        # Potenciál (16 módos tájkép)
        self.V_static = self._create_16mode_landscape()
        # Barrier management: dict of {id: V_field}
        self.active_barriers = {} 
        self.V_coupling = np.zeros_like(self.V_static)
        self._update_total_potential()
        
        # Fizika paraméterek
        self.g = -1.0      # Attraktív (bright soliton)
        self.dt = 0.01     # Időlépés
        self.gamma = 0.01  # Csillapítás (felejtés)
        self.kinetic_scale = 1.0 # Viszkozitás inverze (1.0 = szuperfolyékony)
        
        # Hope Genome nevek
        self.mode_names = [
            "Brain", "Heart", "Soul", "Executor",
            "Memory", "Logic", "Intuition", "Ethics",
            "Feeling", "Creator", "Communicator", "Sensor",
            "Motor", "Mirror", "Learner", "Architect"
        ]

        # ═══ 16 ÁLLÓHULLÁM MÓD ═══
        self.modes = self._define_standing_wave_modes()
        
        # ═══ ÁLLAPOT ═══
        self.time = 0.0
        self.history = []
    
    def _initialize_field(self):
        """
        Kezdeti hullámfüggvény: 2D Gauss csomag
        """
        σ = 2.0
        ψ0 = np.exp(-(self.X**2 + self.Y**2)/(2*σ**2))
        
        # Normalizálás
        norm = np.sqrt(np.sum(np.abs(ψ0)**2) * self.dx**2)
        
        return ψ0 / norm
    
    def _create_16mode_landscape(self):
        """
        16 potenciálgödör 2D-ben - HATSZÖG RÁCS!
        (Természetesebb mint négyzetes)
        """
        V = 0.05 * (self.X**2 + self.Y**2)  # Harmonikus csapda
        
        # 16 Gauss-gödör hatszög elrendezésben
        positions = self._hexagonal_lattice(n=16, radius=6.0)
        
        for (x0, y0) in positions:
            V += -2.0 * np.exp(-((self.X-x0)**2 + (self.Y-y0)**2)/2.0)
        
        return V
    
    def add_coupling(self, mode_name1, mode_name2, strength=1.0):
        """
        Tájkép-formálás: Csatorna nyitása két mód között
        Ez csökkenti a potenciálgátat, engedve az áramlást.
        """
        idx1 = next((i for i, m in enumerate(self.modes) if m['name'] == mode_name1), None)
        idx2 = next((i for i, m in enumerate(self.modes) if m['name'] == mode_name2), None)
        
        if idx1 is None or idx2 is None:
            print(f"⚠️ Hiba: Nem található mód ({mode_name1} vagy {mode_name2})")
            return
            
        pos1 = self.modes[idx1]['position']
        pos2 = self.modes[idx2]['position']
        
        # Vonal mentén Gauss-csatorna (negatív potenciál)
        # Parametrikus vonal: p = (1-t)*p1 + t*p2
        # De egyszerűbb egy hosszúkás Gauss-t ráilleszteni
        
        mid_x = (pos1[0] + pos2[0]) / 2
        mid_y = (pos1[1] + pos2[1]) / 2
        
        dx = pos2[0] - pos1[0]
        dy = pos2[1] - pos1[1]
        length = np.sqrt(dx**2 + dy**2)
        angle = np.arctan2(dy, dx)
        
        # Forgatott koordináták a csatorna középpontjához képest
        X_rot = (self.X - mid_x) * np.cos(angle) + (self.Y - mid_y) * np.sin(angle)
        Y_rot = -(self.X - mid_x) * np.sin(angle) + (self.Y - mid_y) * np.cos(angle)
        
        # Csatorna potenciál: hosszú a hossztengely mentén, keskeny keresztben
        channel_V = -strength * np.exp(-(X_rot**2/(length**2) + Y_rot**2/0.5))
        
        self.V_coupling += channel_V
        self._update_total_potential()
        print(f"🔗 Kapcsolat létrehozva: {mode_name1} <==> {mode_name2} (erősség: {strength})")

    def _update_total_potential(self):
        """Összegzi a potenciál komponenseket"""
        V_barriers_total = np.zeros_like(self.V_static)
        for b in self.active_barriers.values():
            V_barriers_total += b
            
        self.V = self.V_static + V_barriers_total + self.V_coupling

    def add_barrier(self, position, strength=0.5, width=1.0, barrier_id=None):
        """
        Lokális gát építése (pl. a Brain köré)
        barrier_id: egyedi azonosító a későbbi módosításhoz
        """
        x0, y0 = position
        if barrier_id is None:
            barrier_id = f"barrier_{x0}_{y0}"
        
        # Pozitív Gauss-potenciál
        barrier = strength * np.exp(-((self.X-x0)**2 + (self.Y-y0)**2)/(2*width**2))
        
        self.active_barriers[barrier_id] = barrier
        self._update_total_potential()
        print(f"🛡️ Gát építve: ID={barrier_id}, pos={position}, H={strength}, W={width}")

    def set_barrier(self, position, strength=0.5, width=1.0, barrier_id=None):
        """
        Gát beállítása (előző törlése/felülírása)
        Ugyanaz mint add_barrier, csak kifejezőbb név a szabályozáshoz
        """
        self.add_barrier(position, strength, width, barrier_id)

    def get_mode_position(self, mode_name):
        """Segédfüggvény pozíció lekéréshez"""
        for mode in self.modes:
            if mode['name'] == mode_name:
                return mode['position']
        return None

    def _hexagonal_lattice(self, n, radius):
        """16 pont hatszög rácsban"""
        positions = [(0, 0)]  # Központ
        
        # 6 pont a belső gyűrűben
        for i in range(6):
            angle = i * np.pi / 3
            x = radius * 0.5 * np.cos(angle)
            y = radius * 0.5 * np.sin(angle)
            positions.append((x, y))
        
        # 9 pont a külső gyűrűben
        for i in range(9):
            angle = i * 2*np.pi / 9
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            positions.append((x, y))
        
        return positions[:n]
    
    def _define_standing_wave_modes(self):
        """
        16 állóhullám mód definíció
        Ezek NEM komponensek - MINTÁZATOK a mezőben!
        """
        positions = self._hexagonal_lattice(16, 6.0)
        
        modes = []
        for i, (x0, y0) in enumerate(positions):
            # Minden mód = Gauss * e^(iθ)
            mode_pattern = lambda X, Y, x0=x0, y0=y0, m=i: \
                np.exp(-((X-x0)**2 + (Y-y0)**2)/4.0) * \
                np.exp(1j * m * np.arctan2(Y-y0, X-x0))
            
            modes.append({
                'index': i,
                'name': self.mode_names[i] if i < len(self.mode_names) else f"M{i+1}",
                'position': (x0, y0),
                'pattern': mode_pattern,
                'frequency': 0.5 + i * 0.1  # Különböző frekvenciák
            })
        
        return modes
    
    @staticmethod
    @jit
    def _gpe_step_2d(ψ, V, g, dt, K2, gamma, kinetic_scale):
        """
        2D GPE lépés Split-Step Fourier-rel
        kinetic_scale: módosítja a diszperziót (viszkozitás szimuláció)
        """
        # Fél kinetic (skálázva)
        ψ_k = jnp.fft.fft2(ψ)
        ψ_k = ψ_k * jnp.exp(-1j * dt * K2 * kinetic_scale / 4)
        ψ = jnp.fft.ifft2(ψ_k)
        
        # Teljes potential + nonlinear + damping
        V_total = V + g * jnp.abs(ψ)**2
        ψ = ψ * jnp.exp(-1j * dt * V_total - gamma * dt)
        
        # Fél kinetic (skálázva)
        ψ_k = jnp.fft.fft2(ψ)
        ψ_k = ψ_k * jnp.exp(-1j * dt * K2 * kinetic_scale / 4)
        ψ = jnp.fft.ifft2(ψ_k)
        
        return ψ
    
    def set_viscosity(self, level):
        """
        Viszkozitás beállítása (0.0 = Szuperfolyékony, 1.0 = Ragadós)
        Belül: kinetic_scale 1.0 -> 0.1
        """
        # Ha level=0 (flow), scale=1.0
        # Ha level=1 (ragad), scale=0.1
        self.kinetic_scale = 1.0 - (0.9 * np.clip(level, 0.0, 1.0))
        print(f"💧 Viszkozitás beállítva: {level:.2f} (Kinetic Scale: {self.kinetic_scale:.2f})")

    def get_state_metrics(self):
        """
        Állapotlekérés az RL ágensnek
        Return: (brain_energy, entropy)
        """
        energies = self.measure_mode_energies()
        brain_energy = energies[0] # Brain mode
        
        # Shannon entrópia a 16 mód eloszlásán
        # Normalizáljuk az eloszlást
        p = energies / np.sum(energies)
        p = p[p > 0] # 0 kivétele log miatt
        entropy = -np.sum(p * np.log(p))
        
        return brain_energy, entropy

    def evolve(self, steps=100):
        """
        Mező fejlődés
        """
        # Convert to JAX arrays once for the loop if possible, 
        # but here we keep the user's structure (interleaving numpy/jax) 
        # to test their exact logic first.
        # However, to make it run smoothly with JAX JIT, we pass jax arrays.
        
        # Pre-convert constant fields to JAX arrays for efficiency
        j_V = jnp.array(self.V)
        j_K2 = jnp.array(self.K2)
        
        current_psi = jnp.array(self.ψ)
        
        for _ in range(steps):
            current_psi = self._gpe_step_2d(
                current_psi,
                j_V,
                self.g,
                self.dt,
                j_K2,
                self.gamma,
                self.kinetic_scale
            )
            self.time += self.dt
            
        self.ψ = np.array(current_psi) # Vissza numpy-ba
        
        # Normalizálás
        norm = np.sqrt(np.sum(np.abs(self.ψ)**2) * self.dx**2)
        self.ψ = self.ψ / norm

    
    def excite_mode(self, mode_index, strength=1.0):
        """
        Egy mód gerjesztése - REZONANCIA!
        """
        mode = self.modes[mode_index]
        pattern = mode['pattern'](self.X, self.Y)
        
        # Fázisrúgás a mező aktuális állapotán
        self.ψ = self.ψ * np.exp(1j * strength * np.real(pattern))
        
        # Normalizálás
        norm = np.sqrt(np.sum(np.abs(self.ψ)**2) * self.dx**2)
        self.ψ = self.ψ / norm
    
    def measure_mode_energies(self):
        """
        Az energia eloszlás a 16 mód között
        
        Ez a "demokratikus szavazás"!
        """
        density = np.abs(self.ψ)**2
        
        energies = []
        for mode in self.modes:
            x0, y0 = mode['position']
            
            # Gauss súly a mód körül
            weight = np.exp(-((self.X-x0)**2 + (self.Y-y0)**2)/4.0)
            
            # Energia = súlyozott integráció
            energy = np.sum(density * weight) * self.dx**2
            
            energies.append(energy)
        
        # Normalizálás
        energies = np.array(energies)
        return energies / (np.sum(energies) + 1e-10)
    
    def coherence(self):
        """
        Koherencia mérés
        """
        density = np.abs(self.ψ)**2
        
        max_density = np.max(density)
        mean_density = np.mean(density)
        
        return np.tanh(max_density / (mean_density * 15))
    
    def hope_genome_vote(self):
        """
        A Hope Genome "szavazás" = rezonancia mérés
        """
        energies = self.measure_mode_energies()
        coherence = self.coherence()
        
        # Top 3 mód
        top_3 = np.argsort(energies)[-3:][::-1]
        
        result = {
            'energies': energies,
            'coherence': coherence,
            'dominant_modes': [
                {
                    'index': int(i),
                    'name': self.modes[i]['name'],
                    'energy': float(energies[i])
                }
                for i in top_3
            ]
        }
        
        return result
    
    def emotimem_store(self, experience_position, emotion_intensity, emotion_valence):
        """
        EmotiMem: Hullámcsomag létrehozása
        
        experience_position: (x, y) hol a "szemantikai térben"
        emotion_intensity: mennyire erős
        emotion_valence: pozitív/negatív (fázis)
        """
        x0, y0 = experience_position
        
        # Lokalizált hullámcsomag
        σ = 1.0 / emotion_intensity  # Intenzív = lokalizált
        phase = emotion_valence * np.pi  # Pozitív/negatív
        
        memory_packet = emotion_intensity * \
                       np.exp(-((self.X-x0)**2 + (self.Y-y0)**2)/(2*σ**2)) * \
                       np.exp(1j * phase)
        
        # BELESIMUL A MEZŐBE
        self.ψ = self.ψ + 0.1 * memory_packet
        
        # Normalizálás
        norm = np.sqrt(np.sum(np.abs(self.ψ)**2) * self.dx**2)
        self.ψ = self.ψ / norm
        
        print(f"💾 Emlék tárolva: ({x0:.1f}, {y0:.1f}), I={emotion_intensity:.2f}")
    
    def emotimem_recall(self, context_position, evolution_steps=50):
        """
        EmotiMem: Visszaidézés rezonanciával
        """
        x0, y0 = context_position
        
        # Kontextus gerjesztés
        context_wave = np.exp(-((self.X-x0)**2 + (self.Y-y0)**2)/8.0)
        self.ψ = self.ψ + 0.2 * context_wave
        
        # Normalizálás
        norm = np.sqrt(np.sum(np.abs(self.ψ)**2) * self.dx**2)
        self.ψ = self.ψ / norm
        
        # Hagy időt a rezonanciának
        self.evolve(steps=evolution_steps)
        
        # Megnézzük mi aktiválódott
        density = np.abs(self.ψ)**2
        
        # Csúcsok keresése (emlékek)
        from scipy.ndimage import maximum_filter
        local_max = maximum_filter(density, size=5)
        peaks = (density == local_max) & (density > np.mean(density) * 2)
        
        recalled_memories = []
        y_peaks, x_peaks = np.where(peaks)
        
        for xp, yp in zip(x_peaks[:5], y_peaks[:5]):  # Top 5
            x_pos = self.X[0, xp]
            y_pos = self.Y[yp, 0]
            intensity = density[yp, xp]
            
            recalled_memories.append({
                'position': (x_pos, y_pos),
                'intensity': intensity
            })
        
        print(f"🔍 {len(recalled_memories)} emlék aktiválódott")
        
        return recalled_memories
    
    def meditate(self, steps=100):
        """
        Meditáció: alapállapot keresés
        """
        print("🧘 Meditáció...")
        
        # Imaginárius idő evolúció
        # We need to convert to numpy for the roll operations or use jnp.roll
        # Let's stick to numpy as per original code for this part, or update to JAX.
        # The original code used numpy roll.
        
        for _ in range(steps):
            # Laplacian (finite difference)
            ψ_xx = (np.roll(self.ψ, 1, 0) + np.roll(self.ψ, -1, 0) - 2*self.ψ) / self.dx**2
            ψ_yy = (np.roll(self.ψ, 1, 1) + np.roll(self.ψ, -1, 1) - 2*self.ψ) / self.dx**2
            
            # Hamiltonian
            V_total = self.V + self.g * np.abs(self.ψ)**2
            H_ψ = -0.5 * (ψ_xx + ψ_yy) + V_total * self.ψ
            
            # Imaginárius lépés
            self.ψ = self.ψ - self.dt * H_ψ
            
            # Normalizálás
            norm = np.sqrt(np.sum(np.abs(self.ψ)**2) * self.dx**2)
            self.ψ = self.ψ / norm
        
        coherence = self.coherence()
        print(f"✨ Koherencia: {coherence:.3f}")
    
    def visualize(self):
        """
        Vizualizáció
        """
        import matplotlib.pyplot as plt
        
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        
        # 1. Kognitív sűrűség
        density = np.abs(self.ψ)**2
        im1 = axes[0].imshow(density, extent=[-self.L/2, self.L/2]*2,
                            origin='lower', cmap='viridis')
        axes[0].set_title('Kognitív Mező Sűrűség |Ψ|²')
        plt.colorbar(im1, ax=axes[0])
        
        # Mód pozíciók
        for mode in self.modes[:16]:
            x0, y0 = mode['position']
            axes[0].plot(x0, y0, 'r*', markersize=10)
            axes[0].text(x0, y0+0.5, mode['name'], ha='center',
                        fontsize=7, color='white',
                        bbox=dict(boxstyle='round', facecolor='black', alpha=0.5))
        
        # 2. Potenciál tájkép
        im2 = axes[1].imshow(self.V, extent=[-self.L/2, self.L/2]*2,
                            origin='lower', cmap='coolwarm')
        axes[1].set_title('Potenciál Tájkép V(x,y)')
        plt.colorbar(im2, ax=axes[1])
        
        # 3. Mód energiák
        energies = self.measure_mode_energies()
        bars = axes[2].bar(range(16), energies, color='steelblue', alpha=0.7)
        
        # Top 3 kiemelése
        top_3 = np.argsort(energies)[-3:]
        for idx in top_3:
            bars[idx].set_color('coral')
        
        axes[2].set_xlabel('Mód Index')
        axes[2].set_ylabel('Energia')
        axes[2].set_title(f'Mód Aktiváció (C={self.coherence():.3f})')
        axes[2].set_xticks(range(16))
        axes[2].set_xticklabels([m['name'][:3] for m in self.modes], rotation=45)
        axes[2].grid(alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.savefig('fluid_stratos_viz.png')
        print("📊 Visualization saved to fluid_stratos_viz.png")

    def animate_evolution(self, steps=200, filename='fluid_evolution.gif', interval=50):
        """
        Animáció készítése a mező fejlődéséről
        """
        import matplotlib.animation as animation
        from matplotlib.animation import PillowWriter
        
        print(f"🎬 Animáció generálása ({steps} lépés)...")
        
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.set_title("Kognitív Mező Áramlása")
        
        # Kezdeti állapot plot
        density = np.abs(self.ψ)**2
        im = ax.imshow(density, extent=[-self.L/2, self.L/2]*2,
                      origin='lower', cmap='viridis', vmin=0, vmax=np.max(density)*0.8)
        
        # Módok jelölése
        for mode in self.modes:
            x0, y0 = mode['position']
            ax.plot(x0, y0, 'r.', markersize=2, alpha=0.5)
            # ax.text(x0, y0, mode['name'][:2], color='white', fontsize=6, alpha=0.5)

        # JAX optimalizáció miatt konvertáljuk a konstansokat
        j_V = jnp.array(self.V)
        j_K2 = jnp.array(self.K2)
        current_psi = jnp.array(self.ψ)

        def update(frame):
            nonlocal current_psi
            # 5 fizikai lépés per frame az animáció sebességéért
            for _ in range(5):
                current_psi = self._gpe_step_2d(
                    current_psi, j_V, self.g, self.dt, j_K2, self.gamma
                )
            
            # Megjelenítés
            psi_np = np.array(current_psi)
            density = np.abs(psi_np)**2
            im.set_data(density)
            return [im]

        ani = animation.FuncAnimation(fig, update, frames=steps//5, blit=True, interval=interval)
        
        writer = PillowWriter(fps=15)
        ani.save(filename, writer=writer)
        
        # Állapot frissítése a végén
        self.ψ = np.array(current_psi)
        norm = np.sqrt(np.sum(np.abs(self.ψ)**2) * self.dx**2)
        self.ψ = self.ψ / norm
        
        print(f"💾 Animáció mentve: {filename}")


# ═══════════════════════════════════════════════════════════════
# DEMO
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("🌊 FLUID STRATOS - A Folyékony Manifestáció")
    print("="*60)
    
    # Rendszer létrehozása
    stratos = FluidSTRATOS(grid_size=(64, 64))
    
    print("\n1️⃣ Kezdeti állapot:")
    vote = stratos.hope_genome_vote()
    for mode in vote['dominant_modes']:
        print(f"   {mode['name']:12s}: {mode['energy']:.3f}")
    print(f"   Koherencia: {vote['coherence']:.3f}")
    
    # Brain mód gerjesztése
    print("\n2️⃣ Brain (Analitikus) mód gerjesztése...")
    stratos.excite_mode(0, strength=2.0)
    stratos.evolve(steps=100)
    
    vote = stratos.hope_genome_vote()
    for mode in vote['dominant_modes']:
        print(f"   {mode['name']:12s}: {mode['energy']:.3f}")
    
    # EmotiMem demo
    print("\n3️⃣ EmotiMem: Emlék tárolás...")
    stratos.emotimem_store(
        experience_position=(3.0, 4.0),
        emotion_intensity=0.8,
        emotion_valence=1.0  # Pozitív
    )
    
    stratos.evolve(steps=50)
    
    print("\n4️⃣ EmotiMem: Visszaidézés...")
    memories = stratos.emotimem_recall(
        context_position=(3.5, 4.2)
    )
    
    for i, mem in enumerate(memories):
        print(f"   Emlék {i+1}: pos={mem['position']}, I={mem['intensity']:.3f}")
    
    # Meditáció
    print("\n5️⃣ Meditáció (koherencia visszaállítás)...")
    stratos.meditate(steps=50)
    
    # Vizualizáció
    print("\n6️⃣ Vizualizáció...")
    stratos.visualize()

    # Új Funkciók Demo
    print("\n🌊 BŐVÍTETT DEMO: Tájkép-formálás és Animáció")
    print("="*60)
    
    # Új tiszta rendszer
    stratos_fluid = FluidSTRATOS(grid_size=(64, 64))
    
    # 1. "Brain Shield" (Védőgát) építése
    # A központi elszívás csökkentésére (ε=0.5 a demóban a láthatóságért)
    print("🛡️ Brain Shield építése (gát a központ körül)...")
    stratos_fluid.add_barrier((0,0), strength=0.5, width=2.0)

    # 2. Kapcsolat létrehozása: Intuition <-> Logic
    # Ez egy klasszikus "flow" állapot: az intuíció táplálja a logikát
    stratos_fluid.add_coupling("Intuition", "Logic", strength=5.0)
    
    # 3. Intuíció gerjesztése
    print("⚡ Intuíció gerjesztése...")
    stratos_fluid.excite_mode(6, strength=3.0) # 6 = Intuition indexe kb
    
    # 4. Animáció a folyásról
    # Látnunk kell, ahogy az energia átfolyik a csatornán a Logikába
    stratos_fluid.animate_evolution(steps=300, filename='flow_intuition_logic.gif')
    
    vote = stratos_fluid.hope_genome_vote()
    print("Végállapot módok:")
    for mode in vote['dominant_modes']:
        print(f"   {mode['name']:12s}: {mode['energy']:.3f}")

    print("\n✨ Bővített Demo kész")
