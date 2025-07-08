# step7_full_ga.py

import random
import numpy as np
from deap import tools
from step5_toolbox import toolbox
from step1_setup import x_s, y_s

POP_SIZE = 100
N_GEN    = 100
CXPB     = 0.7
MUTPB    = 0.2

def ga_run():
    # initialize population
    pop = toolbox.population(n=POP_SIZE)
    # setup hall of fame
    hof = tools.HallOfFame(maxsize=5)
    # evaluate initial population
    for ind in pop:
        ind.fitness.values = toolbox.evaluate(ind, x_s, y_s)
        ind.generation = 0

    for gen in range(1, N_GEN+1):
        # selection
        offspring = toolbox.select(pop, len(pop))
        offspring = list(map(toolbox.clone, offspring))
        # crossover
        for c1, c2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(c1, c2)
                del c1.fitness.values; del c2.fitness.values
        # mutation
        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values
        # evaluate invalid individuals
        invalid = [ind for ind in offspring if not ind.fitness.valid]
        for ind in invalid:
            ind.fitness.values = toolbox.evaluate(ind, x_s, y_s)
        # replacement
        pop[:] = offspring
        
        # update generation
        for ind in pop:
            ind.generation = gen
            
        # update hall of fame
        hof.update(pop)
        
        # statistics
        fits = [ind.fitness.values[0] for ind in pop]
        print(f"Gen {gen}: Best={min(fits):.2f}, Avg={np.mean(fits):.2f}")

    best = tools.selBest(pop, 1)[0]
    print("Best individual:", best)
    print("Best time:", best.fitness.values[0])
    print("Hall of Fame:")
    for i, ind in enumerate(hof):
        fit = ind.fitness.values[0]
        print("individual: ", ind)
        print(f"Gen {ind.generation}: Best={min(fits):.2f}, Avg={np.mean(fits):.2f}")
    
if __name__ == "__main__":
    ga_run()
