"""
EMOTIMEM DEMO - Memory Storage and Recall

This example demonstrates how Fluid STRATOS handles memories:
1. Storing emotional experiences as wave packets
2. Contextual recall through resonance
3. Interference patterns as associations
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fluid_stratos import FluidSTRATOS
import numpy as np


def main():
    print("💾 EMOTIMEM SYSTEM - Memory Demo")
    print("=" * 60)

    # Create the system
    print("\n1️⃣ Initializing cognitive field...")
    stratos = FluidSTRATOS(grid_size=(128, 128))

    # Store multiple memories
    print("\n2️⃣ Storing emotional memories...")

    memories_to_store = [
        {
            'name': 'Happy Birthday',
            'position': (3.0, 4.0),
            'intensity': 0.9,
            'valence': 1.0,  # Positive
            'description': 'A joyful celebration'
        },
        {
            'name': 'First Heartbreak',
            'position': (-2.0, 3.5),
            'intensity': 0.8,
            'valence': -1.0,  # Negative
            'description': 'A painful experience'
        },
        {
            'name': 'Learning to Code',
            'position': (5.0, -1.0),
            'intensity': 0.7,
            'valence': 0.5,  # Mildly positive
            'description': 'Challenging but rewarding'
        },
        {
            'name': 'Childhood Home',
            'position': (-3.0, -2.0),
            'intensity': 0.6,
            'valence': 0.8,  # Very positive
            'description': 'Nostalgic comfort'
        }
    ]

    for mem in memories_to_store:
        print(f"\n   Storing: {mem['name']}")
        print(f"      Position: {mem['position']}")
        print(f"      Intensity: {mem['intensity']} | Valence: {mem['valence']:+.1f}")
        print(f"      '{mem['description']}'")

        stratos.emotimem_store(
            experience_position=mem['position'],
            emotion_intensity=mem['intensity'],
            emotion_valence=mem['valence']
        )

        # Let the memory settle
        stratos.evolve(steps=20)

    # Let the system stabilize
    print("\n3️⃣ Allowing memories to stabilize...")
    stratos.evolve(steps=100)

    # Recall memories by context
    print("\n4️⃣ Recalling memories by context...\n")

    contexts = [
        {
            'name': 'Thinking about celebrations',
            'position': (3.5, 4.2),  # Near "Happy Birthday"
        },
        {
            'name': 'Feeling sad',
            'position': (-2.5, 3.0),  # Near "First Heartbreak"
        },
        {
            'name': 'Remembering learning experiences',
            'position': (4.5, -0.5),  # Near "Learning to Code"
        }
    ]

    for ctx in contexts:
        print(f"Context: {ctx['name']}")
        print(f"   Probing position: {ctx['position']}")

        recalled = stratos.emotimem_recall(
            context_position=ctx['position'],
            evolution_steps=50
        )

        print(f"   Activated {len(recalled)} memory region(s):")
        for i, rec in enumerate(recalled[:3]):  # Top 3
            print(f"      #{i+1}: Position {rec['position']}, "
                  f"Intensity {rec['intensity']:.4f}")

        print()

    # Visualize the final state
    print("5️⃣ Creating visualization...")
    stratos.visualize()
    print("   Saved to: fluid_stratos_viz.png")

    print("\n✨ EmotiMem Demo complete!")
    print("\nKey insights:")
    print("• Memories are stored as localized wave packets")
    print("• Emotional intensity affects memory localization (sharper = more intense)")
    print("• Valence is encoded in the phase (positive/negative)")
    print("• Similar contexts trigger resonance with related memories")
    print("• Multiple memories can interfere, creating associations")


if __name__ == "__main__":
    main()
