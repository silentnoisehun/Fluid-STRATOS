"""
BARRIER & CHANNEL DEMO - Landscape Shaping

This example demonstrates how to shape the cognitive landscape:
1. Building protective barriers around modes
2. Opening channels between modes
3. Observing energy flow patterns
4. The "Brain Shield" + "Intuition-Logic Channel" configuration
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fluid_stratos import FluidSTRATOS


def main():
    print("🛡️ BARRIER & CHANNEL SHAPING - Landscape Demo")
    print("=" * 60)

    # Create system
    print("\n1️⃣ Creating cognitive field...")
    stratos = FluidSTRATOS(grid_size=(64, 64))

    # Initial state
    print("\n2️⃣ Initial state (no barriers or channels):")
    vote = stratos.hope_genome_vote()
    print(f"   Top 3 modes:")
    for mode in vote['dominant_modes']:
        print(f"      {mode['name']:12s}: {mode['energy']:.4f}")

    # Build Brain Shield
    print("\n3️⃣ Building Brain Shield...")
    print("   Purpose: Protect Brain from being drained by the central harmonic trap")

    stratos.add_barrier(
        position=(0, 0),        # Brain is at center
        strength=0.8,           # Moderate barrier height
        width=2.0,              # Barrier width
        barrier_id="brain_shield"
    )

    print("   Brain Shield active!")

    # Open Intuition-Logic Channel
    print("\n4️⃣ Opening Intuition ↔ Logic channel...")
    print("   Purpose: Create a flow pathway for intuitive insights to inform logic")

    stratos.add_coupling(
        mode_name1="Intuition",
        mode_name2="Logic",
        strength=3.0  # Channel depth
    )

    print("   Channel established!")

    # Excite Intuition
    print("\n5️⃣ Exciting Intuition mode...")
    intuition_idx = next(i for i, m in enumerate(stratos.modes) if m['name'] == "Intuition")
    stratos.excite_mode(intuition_idx, strength=4.0)
    print(f"   Intuition (mode {intuition_idx}) excited with strength 4.0")

    # Evolve and observe flow
    print("\n6️⃣ Evolving system to observe energy flow...")

    checkpoints = [0, 50, 100, 200]

    for i, steps in enumerate(checkpoints):
        if i == 0:
            continue

        stratos.evolve(steps=steps - checkpoints[i-1])

        vote = stratos.hope_genome_vote()
        print(f"\n   After {steps} steps (t={stratos.time:.2f}):")
        print(f"   Coherence: {vote['coherence']:.3f}")

        energies = stratos.measure_mode_energies()

        # Find Intuition and Logic energies
        intuition_energy = energies[intuition_idx]
        logic_idx = next(i for i, m in enumerate(stratos.modes) if m['name'] == "Logic")
        logic_energy = energies[logic_idx]
        brain_energy = energies[0]

        print(f"   Intuition: {intuition_energy:.4f}")
        print(f"   Logic:     {logic_energy:.4f}")
        print(f"   Brain:     {brain_energy:.4f}")

    # Final state
    print("\n7️⃣ Final state:")
    vote = stratos.hope_genome_vote()
    print(f"   Top 3 modes:")
    for mode in vote['dominant_modes']:
        print(f"      {mode['name']:12s}: {mode['energy']:.4f}")

    # Visualize
    print("\n8️⃣ Creating visualization...")
    stratos.visualize()
    print("   Saved to: fluid_stratos_viz.png")

    print("\n✨ Barrier & Channel Demo complete!")
    print("\nKey insights:")
    print("• Barriers prevent energy drainage from important modes")
    print("• Channels facilitate energy flow between related modes")
    print("• Energy flows from excited regions through channels")
    print("• The Brain Shield maintains analytical capacity during intuitive bursts")
    print("• Intuition-Logic coupling enables 'aha!' moments")

    print("\n💡 Try experimenting:")
    print("• Change barrier strength (0.0-2.0)")
    print("• Adjust channel depth (1.0-5.0)")
    print("• Excite different modes")
    print("• Create multiple channels (e.g., Heart-Ethics, Memory-Learner)")


if __name__ == "__main__":
    main()
