# Motorbike Lap Optimization with Genetic Algorithms

## Overview
This project uses Genetic Algorithms to optimize motorcycle lap times on a closed circuit. It's a proof-of-concept study demonstrating how AI can discover better racing trajectories than basic heuristics.

## Current Status
- ✅ Track visualization with spline interpolation
- ✅ Physics simulation with speed profiles
- ✅ Animation showing acceleration/braking points (colored path)
- ✅ Lap time estimation
- 🚧 Genetic Algorithm optimization (in progress)

## Quick Start
```bash
# Install conda (if not already installed)
conda activate ag_motorbike
python src/visualization.py  # Watch animated lap simulation
python src/main.py --track-location tracks/waypoints_S.csv  # Plot track with lap time
```

## Project Goals
- **Primary**: Minimize lap time using Genetic Algorithms
- **Research Questions**:
  - Can GA discover better trajectories than baseline approaches?
  - How do GA parameters affect convergence and solution quality?
  - What's the trade-off between model simplicity and optimization performance?

## Technical Approach

### 1. Track Representation
- Load waypoints from CSV files
- Generate smooth splines using SciPy
- Discretize into segments for physics simulation

### 2. Physics Model
- Simplified point-mass dynamics
- Curvature-based speed limits from friction constraints
- Forward/backward pass speed optimization

### 3. Genetic Algorithm (Planned)
- **Chromosome**: Lateral offsets or control points along track
- **Fitness**: Lap time + penalty for physics violations
- **Operators**: Tournament selection, uniform crossover, Gaussian mutation

## Project Structure
```
src/
├── main.py           # Main entry point
├── track_loader.py   # Track loading and visualization
├── dynamics.py       # Physics simulation
└── visualization.py  # Animated lap visualization

tracks/               # Track data files
├── waypoints_S.csv   # Sample track
```

## Development Timeline (6 weeks)
| Week | Focus |
|------|-------|
| 1-2  | Track loading, physics simulation |
| 3-4  | Genetic Algorithm implementation |
| 5    | Parameter tuning and experiments |
| 6    | Analysis and documentation |

## Technologies
- **Python 3.9** with Conda
- **NumPy/SciPy** for numerical computation
- **Matplotlib** for visualization
- **DEAP** for Genetic Algorithms (planned)

## Known Issues
- Wayland display issues on WSL2 (use `export DISPLAY=:0` if needed)
- Animation requires GUI backend for matplotlib

---
*Academic project for AI course - proof of concept implementation*


