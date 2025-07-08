# step4_setup_deap.py

from deap import base, creator

# 1) Tipo de fitness: FitnessMin, pois queremos *minimizar* lap_time
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))

# 2) Tipo de indivíduo: herda de list e carrega um fitness
creator.create("Individual", list, fitness=creator.FitnessMin)
