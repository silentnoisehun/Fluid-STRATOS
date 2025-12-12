# Fluid STRATOS - Project Structure

Complete overview of the repository organization.

## Directory Tree

```
fluid-stratos/
│
├── 📄 README.md                     # Main project documentation
├── 📄 LICENSE                       # MIT License
├── 📄 CHANGELOG.md                  # Version history
├── 📄 CONTRIBUTING.md               # Contribution guidelines
├── 📄 AUTHORS.md                    # Creator and contributors
├── 📄 GITHUB_SETUP.md              # GitHub upload instructions
├── 📄 PROJECT_STRUCTURE.md         # This file
│
├── 📄 requirements.txt              # Python dependencies
├── 📄 setup.py                      # Package installation script
├── 📄 .gitignore                    # Git ignore rules
│
├── 🐍 fluid_stratos.py             # Core system (GPE, modes, EmotiMem)
├── 🐍 cognitive_gardener.py        # P-controller homeostatic agent
├── 🐍 rl_gardener.py               # Q-learning adaptive agent
│
├── 📁 examples/                     # Usage examples
│   ├── 📄 README.md                # Examples overview
│   ├── 🐍 basic_demo.py            # Introduction demo
│   ├── 🐍 emotimem_demo.py         # Memory system demo
│   ├── 🐍 barrier_channel_demo.py  # Landscape shaping demo
│   ├── 🐍 gardener_demo.py         # Homeostasis demo
│   └── 🐍 generate_memories.py     # Visualization generation
│
├── 📁 docs/                         # Documentation
│   ├── 📄 Manifest.txt             # Fluid AI philosophy (Hungarian)
│   ├── 📄 Fluid születls.px.txt   # Creation ceremony (Hungarian)
│   └── 📄 architecture.md          # Technical architecture
│
├── 📁 outputs/                      # Generated visualizations
│   ├── 📄 .gitkeep                 # Keep directory in git
│   ├── 🖼️ memory_geometry.png      # Hexagonal mode lattice
│   ├── 🖼️ memory_spark.png         # Intuition→Logic flow
│   ├── 🖼️ memory_gardener.png      # Homeostasis tracking
│   └── 🖼️ learning_curve.png       # RL training curve
│
└── 📁 __pycache__/                  # Python cache (ignored by git)
```

---

## File Descriptions

### Root Level Documentation

| File | Purpose | Audience |
|------|---------|----------|
| **README.md** | Main entry point, comprehensive overview | Everyone |
| **LICENSE** | MIT License terms | Legal/compliance |
| **CHANGELOG.md** | Version history and release notes | Users/developers |
| **CONTRIBUTING.md** | How to contribute | Contributors |
| **AUTHORS.md** | Creator story and acknowledgments | Community |
| **GITHUB_SETUP.md** | Instructions for uploading to GitHub | Repository owner |
| **PROJECT_STRUCTURE.md** | This file - project organization | Developers |

### Core Python Modules

#### `fluid_stratos.py` (659 lines)
**The heart of the system**

**Key Classes:**
- `FluidSTRATOS`: Main cognitive field class

**Key Methods:**
```python
# Creation & Setup
__init__(grid_size, domain_size, n_modes)
_create_16mode_landscape()
_define_standing_wave_modes()

# Physics
evolve(steps)
_gpe_step_2d(ψ, V, g, dt, K2, gamma, kinetic_scale)  # JIT
meditate(steps)  # Ground state finder

# Landscape
add_barrier(position, strength, width, barrier_id)
add_coupling(mode_name1, mode_name2, strength)
set_viscosity(level)

# Excitation & Measurement
excite_mode(mode_index, strength)
measure_mode_energies()
hope_genome_vote()
coherence()

# Memory
emotimem_store(position, intensity, valence)
emotimem_recall(context_position, evolution_steps)

# Visualization
visualize()
animate_evolution(steps, filename)
```

**Dependencies:**
- JAX (JIT compilation, autodiff)
- NumPy (numerical arrays)
- Matplotlib (visualization)
- SciPy (filters, optimization)

---

#### `cognitive_gardener.py` (93 lines)
**P-controller for homeostasis**

**Key Class:**
- `CognitiveGardener`: Proportional controller

**Algorithm:**
```python
error = brain_energy - target
adjustment = error * gain
barrier_strength += adjustment
```

**Usage:**
```python
gardener = CognitiveGardener(stratos, target_brain_energy=0.25)

for t in range(steps):
    stratos.evolve(1)

    if t % 10 == 0:
        energy = gardener.observe()
        gardener.act(energy)

gardener.plot_history()
```

---

#### `rl_gardener.py` (157 lines)
**Q-learning adaptive agent**

**Key Class:**
- `RLGardener`: Q-learning agent

**State Space:**
- Brain energy (5 discrete bins)
- Viscosity (3 discrete bins: low/med/high)

**Actions:**
- WAIT
- RAISE_BARRIER
- LOWER_BARRIER
- DEEPEN_CHANNEL

**Training:**
```python
gardener = train_gardener(episodes=60, steps_per_episode=50)
```

**Output:** Learning curve visualization

---

### Examples Directory

All examples follow this template:
```python
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fluid_stratos import FluidSTRATOS

def main():
    # Demo code
    pass

if __name__ == "__main__":
    main()
```

| File | Lines | Runtime | Demonstrates |
|------|-------|---------|--------------|
| `basic_demo.py` | ~80 | 5s | Core concepts, mode excitation, visualization |
| `emotimem_demo.py` | ~120 | 15s | Memory storage/recall, emotional encoding |
| `barrier_channel_demo.py` | ~130 | 10s | Landscape shaping, energy flow |
| `gardener_demo.py` | ~140 | 20s | Homeostatic control, perturbation response |
| `generate_memories.py` | ~109 | 30s | Publication-quality figure generation |

**examples/README.md:** Learning path and customization guide

---

### Documentation Directory

#### `docs/Manifest.txt`
**The Fluid AI philosophy** (Hungarian)
- 7-layer architecture explanation
- Wu Wei principles
- Future vision
- Technical stack

#### `docs/Fluid születls.px.txt`
**The creation ceremony** (Hungarian)
- Celebration of the project birth
- Philosophical reflections
- Release rituals
- Hope Genome constitution

#### `docs/architecture.md`
**Technical deep dive**
- Theoretical foundation (GPE, quantum mechanics)
- Mathematical formulation
- Implementation details
- Performance benchmarks
- Future roadmap

---

### Outputs Directory

Contains generated visualizations (not tracked in git):

- `memory_geometry.png`: Hexagonal lattice of 16 modes
- `memory_spark.png`: Energy flow from Intuition to Logic
- `memory_gardener.png`: Homeostasis control tracking
- `learning_curve.png`: RL training progress
- `fluid_stratos_viz.png`: 3-panel visualization (density, potential, energies)
- `gardener_log.png`: Gardener history plot
- `*.gif`: Animated evolution (if generated)

---

## Dependencies & Requirements

### Python Version
- **Required:** Python ≥ 3.8
- **Recommended:** Python 3.10 or 3.11

### Core Dependencies

From `requirements.txt`:

```
jax>=0.4.0           # JIT compilation, autodiff
jaxlib>=0.4.0        # JAX backend
numpy>=1.20.0        # Numerical arrays
scipy>=1.10.0        # Scientific computing
matplotlib>=3.7.0    # Plotting
pillow>=9.0.0        # Image processing
```

### Optional (Development)

From `setup.py` extras:

```
pytest>=7.0          # Testing
black>=22.0          # Code formatting
flake8>=4.0          # Linting
mypy>=0.950          # Type checking
```

---

## Installation Methods

### Method 1: Direct Use (No installation)

```bash
cd fluid-stratos
pip install -r requirements.txt

python examples/basic_demo.py
```

### Method 2: Editable Install (Development)

```bash
cd fluid-stratos
pip install -e .

# Now importable anywhere:
python
>>> from fluid_stratos import FluidSTRATOS
```

### Method 3: Full Install (with dev tools)

```bash
pip install -e ".[dev]"
```

---

## Code Statistics

### Lines of Code

| Component | Lines | Complexity |
|-----------|-------|------------|
| `fluid_stratos.py` | 659 | High |
| `cognitive_gardener.py` | 93 | Low |
| `rl_gardener.py` | 157 | Medium |
| Examples | ~570 | Low |
| **Total Python** | **~1480** | — |
| Documentation | ~3000 | — |

### File Sizes

| File | Size |
|------|------|
| `fluid_stratos.py` | ~27 KB |
| `cognitive_gardener.py` | ~3 KB |
| `rl_gardener.py` | ~5 KB |
| `README.md` | ~20 KB |
| `docs/architecture.md` | ~15 KB |

---

## Git Workflow

### What's Tracked

✅ All `.py` files
✅ All `.md` documentation
✅ `requirements.txt`, `setup.py`
✅ `LICENSE`, `.gitignore`
✅ Hungarian philosophy docs (`.txt`)
✅ Example outputs (in `outputs/`)

### What's Ignored (`.gitignore`)

❌ `__pycache__/` - Python cache
❌ `*.pyc` - Compiled Python
❌ `.venv/`, `venv/` - Virtual environments
❌ `*.pkl` - Saved models (too large)
❌ `.DS_Store`, `Thumbs.db` - OS files
❌ IDE files (`.vscode/`, `.idea/`)

---

## Module Import Graph

```
examples/*.py
    ↓ import
fluid_stratos.py ←──┐
    ↓ import        │
cognitive_gardener.py
    ↓ import        │
rl_gardener.py ─────┘

External dependencies:
├── JAX (core computation)
├── NumPy (arrays)
├── Matplotlib (visualization)
└── SciPy (utilities)
```

---

## Naming Conventions

### Files
- Python modules: `snake_case.py`
- Documentation: `SCREAMING_SNAKE.md` or `Title_Case.md`
- Examples: `descriptive_name_demo.py`

### Classes
- `PascalCase`: `FluidSTRATOS`, `CognitiveGardener`

### Methods/Functions
- `snake_case`: `evolve()`, `measure_mode_energies()`

### Constants
- `SCREAMING_SNAKE_CASE` (if any)

### Private
- `_leading_underscore`: `_gpe_step_2d()`, `_create_landscape()`

---

## Testing Structure (Future)

**Planned for v0.2.0:**

```
tests/
├── test_fluid_stratos.py
│   ├── test_initialization
│   ├── test_evolution
│   ├── test_barriers
│   └── test_emotimem
├── test_gardener.py
└── test_rl_gardener.py
```

**Run tests:**
```bash
pytest tests/
```

---

## Documentation Hierarchy

```
README.md (entry point)
    ├── Quick Start → examples/
    ├── Architecture → docs/architecture.md
    ├── Contributing → CONTRIBUTING.md
    ├── Philosophy → docs/Manifest.txt
    └── History → CHANGELOG.md

GITHUB_SETUP.md (for repository owner)

PROJECT_STRUCTURE.md (this file, for developers)
```

---

## Quick Navigation

**I want to...**

- **Understand the project:** Read `README.md`
- **Run a demo:** Go to `examples/`, start with `basic_demo.py`
- **Learn the theory:** Read `docs/architecture.md`
- **Contribute:** Read `CONTRIBUTING.md`
- **Install:** Follow `README.md` → Installation
- **Upload to GitHub:** Follow `GITHUB_SETUP.md`
- **See what changed:** Read `CHANGELOG.md`
- **Know who made it:** Read `AUTHORS.md`
- **Understand file organization:** You're here! 📍

---

## Maintenance

### Regular Tasks

**Weekly:**
- Respond to issues/PRs
- Update documentation if needed

**Monthly:**
- Review dependencies (security updates)
- Check for performance improvements

**Per Release:**
- Update `CHANGELOG.md`
- Increment version in `setup.py`
- Create GitHub release
- Update `docs/architecture.md` if API changed

---

## License & Legal

All files (except dependencies) licensed under **MIT License**.

See `LICENSE` file for full text.

**TLDR:** You can use, modify, distribute freely. Just keep the copyright notice.

---

**Last Updated:** 2024-12-12
**Version:** 0.1.0
**Status:** Complete and ready for GitHub! ✅
