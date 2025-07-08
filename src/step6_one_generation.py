# step6_one_generation.py

import numpy as np
from step5_toolbox import toolbox
from step1_setup import x_s, y_s

def one_generation():
    # 1) Cria população
    pop = toolbox.population(n=6)   # só 6 para ficar simples

    # 2) Avalia população
    for ind in pop:
        ind.fitness.values = toolbox.evaluate(ind, x_s, y_s)

    # Exibe os tempos
    times = [ind.fitness.values[0] for ind in pop]
    print("Initial times:", times)

    # 3) Seleção
    offspring = toolbox.select(pop, len(pop))
    print("Selected indices:", [pop.index(i) for i in offspring])

    # 4) Crossover em pares
    child1, child2 = offspring[0].copy(), offspring[1].copy()
    toolbox.mate(child1, child2)
    print("Child1 after crossover:", child1)
    print("Child2 after crossover:", child2)

    # 5) Mutação
    toolbox.mutate(child1)
    print("Child1 after mutation:", child1)

if __name__ == "__main__":
    one_generation()
