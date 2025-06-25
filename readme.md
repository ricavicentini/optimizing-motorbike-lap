# Academic Project: Motorbike Lap Optimization with Genetic Algorithms

## 1. Project Objective  
This is a proof-of-concept study for an academic course in Artificial Intelligence. Our goal is to demonstrate the feasibility of using Genetic Algorithms (GAs) to minimize lap time on a closed motorcycle circuit. Given a simplified physical model of a bike and a digital representation of a race track, we will evolve trajectories that outperform a basic baseline.

Key research questions:  
- Can a GA discover a lap trajectory that improves on a human-inspired or heuristic reference?  
- How do GA parameters (population size, mutation rate, crossover rate) influence convergence speed and solution quality?  
- What is the trade-off between model simplicity (point-mass dynamics) and optimization performance?

## 2. Scope and Constraints  
- **Timeframe:** 6 weeks of active development (25 June – 5 August) with ~5 hours/week.  
- **Model Fidelity:** Simplified “point-mass” or “bicycle” dynamics; no complex tire or suspension models.  
- **Optimization Target:** Single objective—minimize lap time. Secondary metrics (curve smoothness, violation count) may be logged but not optimized.  
- **Proof of Concept:** Code clarity and reproducibility are more important than industrial-grade performance.

## 3. Methodology  
1. **Track Definition**  
   - Load or synthesize waypoints (CSV)  
   - Build a closed spline (Bezier or SciPy `splprep`)  
2. **Dynamics Simulation**  
   - Discretize spline into segments  
   - Compute curvature and maximum cornering speed from friction limit  
   - Integrate a simple point-mass model to estimate lap time  
3. **Genetic Algorithm Design**  
   - **Chromosome:** lateral offsets or control-point perturbations along the track  
   - **Population:** random perturbations around a reference line  
   - **Fitness Function:** simulated lap time + penalty for physics violations  
   - **Operators:** tournament selection, uniform crossover, Gaussian mutation  
   - **Termination:** fixed generation budget or plateau in fitness improvement  
4. **Experimentation**  
   - Tune GA hyperparameters (population size, mutation rate)  
   - Compare best GA solution against baseline trajectory  
   - Analyze convergence curves and sensitivity  

## 4. Deliverables  
- **Source Code Repository** (Python, Conda environment)  
- **Final Report (English)** detailing introduction, methodology, results, discussion, and conclusions  
- **Plots & Tables:**  
  - Evolution of best/average fitness per generation  
  - Overlay of baseline vs. GA-optimized trajectories  
  - Summary of parameter sensitivity  
- **README.md** with setup & usage instructions  

## 5. Timeline (25 June – 5 August)  
| Week | Dates          | Milestone                                    |
|------|----------------|----------------------------------------------|
| 1    | Jun 25–Jul 1   | Environment & track loader; baseline fitness |
| 2    | Jul 2–8        | Dynamics simulation prototype                |
| 3    | Jul 9–15       | GA scaffold (DEAP) + basic fitness integration|
| 4    | Jul 16–22      | GA tuning & debugging                        |
| 5    | Jul 23–29      | Experiments & data collection                |
| 6    | Jul 30–Aug 5   | Report writing & final presentations         |

## 6. Tools & Technologies  
- **Language:** Python 3.9  
- **Conda** (environment management)  
- **NumPy / SciPy** (numerical computation & splines)  
- **Matplotlib / Seaborn** (visualization)  
- **DEAP** (Genetic Algorithm framework)  
- **Git / GitHub** (version control)

## 7. Repository Layout  
