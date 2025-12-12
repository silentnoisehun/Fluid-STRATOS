# Fluid STRATOS Examples

This directory contains example scripts demonstrating various features of Fluid STRATOS.

## Running Examples

From the project root directory:

```bash
# Basic demo
python examples/basic_demo.py

# EmotiMem system
python examples/emotimem_demo.py

# Barrier and channel shaping
python examples/barrier_channel_demo.py

# Cognitive Gardener homeostasis
python examples/gardener_demo.py

# Memory visualization generation
python examples/generate_memories.py
```

## Example Descriptions

### 1. `basic_demo.py` - Introduction

**What it demonstrates:**
- Creating a cognitive field
- Exciting cognitive modes
- Measuring Hope Genome vote
- Basic visualization

**Best for:**
- First-time users
- Understanding core concepts
- Quick system overview

**Runtime:** ~5 seconds

---

### 2. `emotimem_demo.py` - Memory System

**What it demonstrates:**
- Storing emotional memories as wave packets
- Contextual memory recall through resonance
- Interference patterns as associations
- Emotional valence encoding

**Best for:**
- Understanding memory mechanisms
- Exploring associative recall
- Emotional encoding/decoding

**Runtime:** ~15 seconds

**Key concepts:**
- `emotimem_store()`: Store experience with emotion
- `emotimem_recall()`: Context-triggered recall
- Intensity affects localization
- Valence encodes positive/negative

---

### 3. `barrier_channel_demo.py` - Landscape Shaping

**What it demonstrates:**
- Building protective barriers around modes
- Opening flow channels between modes
- Energy flow observation
- Brain Shield + Intuition-Logic configuration

**Best for:**
- Understanding landscape manipulation
- Observing energy dynamics
- Cognitive architecture design

**Runtime:** ~10 seconds

**Key concepts:**
- `add_barrier()`: Create energy barriers
- `add_coupling()`: Open flow channels
- Barriers prevent drainage
- Channels facilitate flow

---

### 4. `gardener_demo.py` - Homeostatic Control

**What it demonstrates:**
- P-controller homeostatic regulation
- Adaptive barrier adjustment
- Perturbation response
- Wu Wei control principle

**Best for:**
- Understanding control mechanisms
- System stability analysis
- Adaptive behavior

**Runtime:** ~20 seconds

**Key concepts:**
- `CognitiveGardener`: Homeostatic agent
- P-controller for regulation
- Target energy maintenance
- Recovery from perturbations

---

### 5. `generate_memories.py` - Visualization Generation

**What it demonstrates:**
- Creating publication-quality visualizations
- Memory geometry (hexagonal lattice)
- Energy flow patterns
- Gardener behavior logging

**Best for:**
- Creating figures for papers/presentations
- Understanding system structure
- Debugging and analysis

**Runtime:** ~30 seconds

**Outputs:**
- `memory_geometry.png`: Hexagonal mode lattice
- `memory_spark.png`: Intuition→Logic flow
- `memory_gardener.png`: Homeostasis tracking

---

## Learning Path

**Recommended order for newcomers:**

1. **Start here:** `basic_demo.py`
   - Get familiar with the system
   - Understand modes and coherence

2. **Next:** `barrier_channel_demo.py`
   - Learn landscape manipulation
   - See energy flow in action

3. **Then:** `emotimem_demo.py`
   - Explore memory mechanisms
   - Understand associations

4. **Advanced:** `gardener_demo.py`
   - See control in action
   - Understand Wu Wei principle

5. **For visualization:** `generate_memories.py`
   - Create your own figures

## Customization Ideas

### For `basic_demo.py`
- Try exciting different modes (Heart, Soul, Intuition)
- Change excitation strength (1.0 - 5.0)
- Vary evolution time (50 - 500 steps)

### For `emotimem_demo.py`
- Add more memories
- Create clusters of related memories
- Test different context positions
- Experiment with valence patterns

### For `barrier_channel_demo.py`
- Build multiple barriers
- Create a network of channels
- Try different barrier strengths
- Observe multi-mode coupling

### For `gardener_demo.py`
- Adjust target energy
- Change control interval
- Add multiple perturbations
- Modify P-controller gain

## Troubleshooting

**"ModuleNotFoundError: No module named 'fluid_stratos'"**
- Run from project root directory
- Or install package: `pip install -e .`

**Slow execution**
- Reduce grid size: `grid_size=(32, 32)`
- Decrease evolution steps
- Check if JAX is using GPU (if available)

**Visualization not saving**
- Ensure `outputs/` directory exists
- Check write permissions
- Install: `pip install matplotlib pillow`

## Contributing Examples

Have a cool example? Please share!

1. Create a new script in `examples/`
2. Add clear comments and docstrings
3. Include output description
4. Update this README
5. Submit a pull request

## Questions?

- Open an issue on GitHub
- Check main README.md
- Read source code comments
