# step5_toolbox.py

import random
from deap import tools
from deap import base
from step4_setup_deap import creator
from step3_evaluation import evaluate

toolbox = base.Toolbox()

# 1) Atributo = offset inicial aleatório em [-2,2] metros
toolbox.register("attr_offset", random.uniform, -2.0, 2.0)

# 2) Indivíduo = repeate attr_offset N times
toolbox.register("individual", tools.initRepeat,
                 creator.Individual, toolbox.attr_offset, n=10)

# 3) População
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# 4) Operadores básicos
toolbox.register("evaluate", evaluate)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=0.5, indpb=0.2)
