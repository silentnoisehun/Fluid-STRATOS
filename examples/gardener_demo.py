"""
COGNITIVE GARDENER DEMO - Homeostatic Control

This example demonstrates the Cognitive Gardener:
1. P-controller for maintaining brain energy homeostasis
2. Adaptive barrier adjustment
3. Response to perturbations
4. Wu Wei control principle
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fluid_stratos import FluidSTRATOS
from cognitive_gardener import CognitiveGardener


def main():
    print("🌿 COGNITIVE GARDENER - Homeostasis Demo")
    print("=" * 60)

    # Initialize system
    print("\n1️⃣ Creating cognitive field and gardener...")

    target_energy = 0.25
    stratos = FluidSTRATOS(grid_size=(64, 64))
    gardener = CognitiveGardener(stratos, target_brain_energy=target_energy)

    print(f"   Target brain energy: {target_energy}")
    print(f"   Initial barrier strength: {gardener.barrier_strength}")

    # Set initial barrier
    stratos.set_barrier((0, 0), strength=0.5, width=2.0, barrier_id="brain_shield")

    # Simulation parameters
    total_steps = 400
    control_interval = 10  # Gardener acts every 10 steps

    print(f"\n2️⃣ Running simulation ({total_steps} steps)...")
    print(f"   Control interval: every {control_interval} steps")

    # Track key moments
    perturbation_time = 200

    for t in range(total_steps):
        # Physics evolution
        stratos.evolve(steps=1)

        # Gardener intervention
        if t % control_interval == 0:
            brain_energy = gardener.observe()
            barrier = gardener.act(brain_energy)
            gardener.log(t, brain_energy, barrier)

            # Status update
            if t % 50 == 0:
                error = brain_energy - target_energy
                print(f"   t={t:3d}: E_brain={brain_energy:.4f} "
                      f"(error: {error:+.4f}), Barrier={barrier:.3f}")

        # External perturbation at t=200
        if t == perturbation_time:
            print(f"\n   ⚡ PERTURBATION at t={t}!")
            print("      Sudden energy burst to Brain mode...")
            stratos.excite_mode(0, strength=2.0)

    # Final statistics
    print("\n3️⃣ Final statistics:")

    brain_energies = gardener.history['brain_energy']
    barriers = gardener.history['barrier']

    import numpy as np

    mean_energy = np.mean(brain_energies)
    std_energy = np.std(brain_energies)
    mean_barrier = np.mean(barriers)

    # Split before/after perturbation
    pre_perturb = brain_energies[:perturbation_time//control_interval]
    post_perturb = brain_energies[perturbation_time//control_interval:]

    std_pre = np.std(pre_perturb)
    std_post = np.std(post_perturb)

    print(f"   Mean brain energy: {mean_energy:.4f} (target: {target_energy})")
    print(f"   Overall std: {std_energy:.4f}")
    print(f"   Std before perturbation: {std_pre:.4f}")
    print(f"   Std after perturbation: {std_post:.4f}")
    print(f"   Mean barrier strength: {mean_barrier:.3f}")

    # Evaluate control quality
    print("\n4️⃣ Control quality assessment:")

    if std_energy < 0.05:
        quality = "Excellent (Wu Wei achieved!)"
    elif std_energy < 0.10:
        quality = "Good"
    elif std_energy < 0.15:
        quality = "Fair"
    else:
        quality = "Needs improvement"

    print(f"   Stability: {quality}")

    recovery_time = None
    for i, e in enumerate(post_perturb):
        if abs(e - target_energy) < 0.05:
            recovery_time = i * control_interval
            break

    if recovery_time:
        print(f"   Recovery time after perturbation: {recovery_time} steps")
    else:
        print(f"   System did not fully recover within simulation time")

    # Plot history
    print("\n5️⃣ Creating visualization...")
    gardener.plot_history()
    print("   Saved to: gardener_log.png")

    print("\n✨ Gardener Demo complete!")
    print("\nKey insights:")
    print("• The Gardener maintains homeostasis through adaptive barriers")
    print("• P-controller adjusts barrier strength based on error")
    print("• System recovers from perturbations automatically")
    print("• Wu Wei: minimal intervention, natural stability")
    print("• Low std (σ < 0.05) indicates mastery of control")

    print("\n💡 Try experimenting:")
    print("• Change target energy (0.1 - 0.4)")
    print("• Adjust P-controller gain (in cognitive_gardener.py)")
    print("• Add multiple perturbations")
    print("• Change control interval")


if __name__ == "__main__":
    main()
