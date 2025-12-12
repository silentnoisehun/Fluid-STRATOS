"""
BASIC DEMO - Introduction to Fluid STRATOS

This example demonstrates the fundamental concepts:
1. Creating a cognitive field
2. Exciting cognitive modes
3. Measuring the Hope Genome vote
4. Visualizing the results
"""

import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fluid_stratos import FluidSTRATOS


def main():
    print("🌊 FLUID STRATOS - Basic Demo")
    print("=" * 60)

    # Step 1: Create the cognitive field
    print("\n1️⃣ Creating the cognitive field...")
    stratos = FluidSTRATOS(grid_size=(64, 64))
    print(f"   Grid size: {stratos.Nx} x {stratos.Ny}")
    print(f"   Domain size: {stratos.L} units")
    print(f"   16 cognitive modes initialized")

    # Step 2: Check initial state
    print("\n2️⃣ Initial state (before any excitation):")
    vote = stratos.hope_genome_vote()
    print(f"   Coherence: {vote['coherence']:.3f}")
    print(f"   Top 3 active modes:")
    for mode in vote['dominant_modes']:
        print(f"      {mode['name']:12s}: {mode['energy']:.4f}")

    # Step 3: Excite the Brain mode
    print("\n3️⃣ Exciting the Brain (Analytical) mode...")
    stratos.excite_mode(0, strength=3.0)
    print("   Applied rezonance strength: 3.0")

    # Step 4: Let the system evolve
    print("\n4️⃣ Evolving the system (200 time steps)...")
    stratos.evolve(steps=200)
    print(f"   System time: {stratos.time:.2f}")

    # Step 5: Check final state
    print("\n5️⃣ Final state (after evolution):")
    vote = stratos.hope_genome_vote()
    print(f"   Coherence: {vote['coherence']:.3f}")
    print(f"   Top 3 active modes:")
    for mode in vote['dominant_modes']:
        print(f"      {mode['name']:12s}: {mode['energy']:.4f}")

    # Step 6: Measure all mode energies
    print("\n6️⃣ All mode energies:")
    energies = stratos.measure_mode_energies()
    for i, mode in enumerate(stratos.modes):
        bar = "█" * int(energies[i] * 100)
        print(f"   {mode['name']:12s}: {bar} {energies[i]:.4f}")

    # Step 7: Visualize
    print("\n7️⃣ Creating visualization...")
    stratos.visualize()
    print("   Saved to: fluid_stratos_viz.png")

    print("\n✨ Demo complete!")
    print("\nKey insights:")
    print("• The cognitive field distributes energy across 16 modes")
    print("• Exciting one mode creates ripples affecting others")
    print("• The system naturally seeks coherent patterns")
    print("• Coherence measures how 'unified' the cognitive state is")


if __name__ == "__main__":
    main()
