"""
COGNITIVE GARDENER - A Tudatos Ágens
"""
from fluid_stratos import FluidSTRATOS
import matplotlib.pyplot as plt
import numpy as np

class CognitiveGardener:
    def __init__(self, system, target_brain_energy=0.20):
        self.system = system
        self.target = target_brain_energy
        self.barrier_strength = 0.5  # Kezdeti gát
        self.brain_index = 0 # Brain is mode 0
        self.history = {'time': [], 'brain_energy': [], 'barrier': []}
        
    def observe(self):
        """Méri a rendszer állapotát"""
        energies = self.system.measure_mode_energies()
        brain_energy = energies[self.brain_index]
        return brain_energy
    
    def act(self, current_brain_energy):
        """Beavatkozik a homeosztázis érdekében"""
        
        # Hiba kiszámítása
        error = current_brain_energy - self.target
        
        # P-szabályozó (Proportional controller)
        # Ha error > 0 (túl sok energia), növeljük a gátat (taszítás)
        # Ha error < 0 (túl kevés energia), csökkentjük a gátat (befolyás)
        adjustment = error * 2.0 
        
        self.barrier_strength += adjustment
        self.barrier_strength = np.clip(self.barrier_strength, 0.0, 2.0)
        
        # Beavatkozás (ID-vel, hogy ne írjon felül más gátakat)
        self.system.set_barrier((0,0), strength=self.barrier_strength, width=2.0, barrier_id="brain_shield")
        
        return self.barrier_strength
    
    def log(self, time, brain_energy, barrier):
        self.history['time'].append(time)
        self.history['brain_energy'].append(brain_energy)
        self.history['barrier'].append(barrier)

    def plot_history(self):
        fig, ax1 = plt.subplots(figsize=(10, 6))
        
        ax1.set_xlabel('Time Steps')
        ax1.set_ylabel('Brain Energy', color='tab:blue')
        ax1.plot(self.history['time'], self.history['brain_energy'], color='tab:blue', label='Brain Energy')
        ax1.axhline(self.target, color='gray', linestyle='--', label='Target')
        ax1.tick_params(axis='y', labelcolor='tab:blue')
        
        ax2 = ax1.twinx()
        ax2.set_ylabel('Barrier Strength', color='tab:orange')
        ax2.plot(self.history['time'], self.history['barrier'], color='tab:orange', linestyle=':', label='Gardener Action')
        ax2.tick_params(axis='y', labelcolor='tab:orange')
        
        plt.title('Cognitive Gardener: Homeosztázis Szabályozás')
        fig.tight_layout()
        plt.savefig('gardener_log.png')
        print("📊 Gardener log saved to gardener_log.png")

if __name__ == "__main__":
    print("🌿 INDUL A KERTÉSZ...")
    stratos = FluidSTRATOS(grid_size=(64, 64))
    gardener = CognitiveGardener(stratos, target_brain_energy=0.25)
    
    # Kezdeti gát
    stratos.set_barrier((0,0), strength=0.5, width=2.0, barrier_id="brain_shield")
    
    # Szimuláció
    steps = 400
    print(f"🔄 Szimuláció futtatása ({steps} lépés)...")
    
    for t in range(steps):
        # 1. Fizika
        stratos.evolve(steps=1)
        
        # 2. Kertész beavatkozása (minden 10. lépésben)
        if t % 10 == 0:
            e_brain = gardener.observe()
            barrier = gardener.act(e_brain)
            gardener.log(t, e_brain, barrier)
            
            # Külső zavarás (perturbáció) a 200. lépésnél
            if t == 200:
                print("⚡ KÜLSŐ ZAVAR: Hirtelen energiafröccs a Brain-be!")
                stratos.excite_mode(0, strength=2.0)
    
    gardener.plot_history()
