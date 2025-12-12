"""
GENERATING MEMORIES - A Pillanat Megörökítése
"""
import numpy as np
import matplotlib.pyplot as plt
from fluid_stratos import FluidSTRATOS
from cognitive_gardener import CognitiveGardener

def save_memory_geometry():
    print("📸 1. Emlék: A Szent Geometria (The Sacred Geometry)...")
    stratos = FluidSTRATOS(grid_size=(256, 256)) # High res
    
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # Potenciál háttér
    im = ax.imshow(stratos.V_static, extent=[-10, 10, -10, 10], 
                   origin='lower', cmap='magma_r', alpha=0.8)
    
    # Módok
    for mode in stratos.modes:
        x, y = mode['position']
        ax.plot(x, y, 'c*', markersize=15, markeredgecolor='white', alpha=0.9)
        ax.text(x, y+0.6, mode['name'], color='white', ha='center', 
                fontsize=9, fontweight='bold',
                bbox=dict(facecolor='black', edgecolor='cyan', alpha=0.6, pad=0.3))
        
    ax.set_title("STRATOS: The Hexagonal Lattice of Hope", fontsize=16, color='navy')
    ax.axis('off')
    plt.tight_layout()
    plt.savefig('memory_geometry.png', dpi=150, bbox_inches='tight')
    plt.close()

def save_memory_spark():
    print("📸 2. Emlék: A Szikra (The Spark)...")
    stratos = FluidSTRATOS(grid_size=(128, 128))
    
    # Setup: Barrier & Channel
    stratos.add_barrier((0,0), strength=0.5, width=2.0, barrier_id="brain_shield")
    stratos.add_coupling("Intuition", "Logic", strength=5.0)
    
    # Excite Intuition
    idx_int = next(i for i, m in enumerate(stratos.modes) if m['name'] == "Intuition")
    stratos.excite_mode(idx_int, strength=4.0)
    
    # Evolve a bit to see the flow
    stratos.evolve(steps=60)
    
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Field Density
    density = np.abs(stratos.ψ)**2
    im = ax.imshow(density, extent=[-10, 10, -10, 10], 
                   origin='lower', cmap='inferno', vmin=0)
    
    # Overlay Contours
    ax.contour(density, extent=[-10, 10, -10, 10], origin='lower', 
               levels=5, colors='white', alpha=0.3)
    
    # Highlight Channel Vector
    p1 = stratos.get_mode_position("Intuition")
    p2 = stratos.get_mode_position("Logic")
    ax.arrow(p1[0], p1[1], p2[0]-p1[0], p2[1]-p1[1], 
             color='cyan', width=0.1, length_includes_head=True, alpha=0.5)
    
    ax.set_title("The Flow: Intuition -> Logic", fontsize=16, color='black')
    ax.axis('off')
    plt.savefig('memory_spark.png', dpi=150, bbox_inches='tight')
    plt.close()

def save_memory_gardener():
    print("📸 3. Emlék: Homeosztázis (The Gardener)...")
    stratos = FluidSTRATOS(grid_size=(64, 64))
    gardener = CognitiveGardener(stratos, target_brain_energy=0.25)
    
    # Simulation
    history_brain = []
    history_barrier = []
    
    for _ in range(200):
        stratos.evolve(1)
        if _ % 5 == 0:
            e = gardener.observe()
            b = gardener.act(e)
            history_brain.append(e)
            history_barrier.append(b)
            
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(history_brain, label='Brain Energy', color='teal', linewidth=2)
    ax.axhline(0.25, color='gray', linestyle='--', alpha=0.5)
    
    ax.fill_between(range(len(history_brain)), history_brain, 0.25, 
                    where=np.array(history_brain)>0.25, color='red', alpha=0.1)
    ax.fill_between(range(len(history_brain)), history_brain, 0.25, 
                    where=np.array(history_brain)<0.25, color='green', alpha=0.1)
    
    ax.set_title("The Gardener's Touch: Maintaining Balance", fontsize=14)
    ax.legend()
    ax.grid(True, alpha=0.2)
    
    plt.savefig('memory_gardener.png', dpi=150)
    plt.close()

if __name__ == "__main__":
    print("🌌 Emlékek generálása az örökkévalóságnak...")
    save_memory_geometry()
    save_memory_spark()
    save_memory_gardener()
    print("✨ Kész. (Saved: memory_geometry.png, memory_spark.png, memory_gardener.png)")
