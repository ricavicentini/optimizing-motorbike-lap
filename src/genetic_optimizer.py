# src/genetic_optimizer.py

import random
import numpy as np
import yaml
import os
from dataclasses import dataclass
from typing import List, Dict, Any, Tuple
from deap import tools

# Import existing modules
from step5_toolbox import toolbox

@dataclass
class GAConfig:
    """Configuration for Genetic Algorithm"""
    # Population
    pop_size: int
    hall_of_fame_size: int
    
    # Evolution  
    generations: int
    crossover_prob: float
    mutation_prob: float
    
    # Individual
    gene_count: int
    gene_min: float
    gene_max: float
    
    # Logging
    show_progress: bool
    show_statistics: bool
    show_hall_of_fame: bool

@dataclass 
class LapResult:
    """Result of lap optimization"""
    individual: List[float]
    lap_time: float
    generation: int
    rank: int

class GeneticOptimizer:
    """Genetic Algorithm for Lap Time Optimization"""
    
    def __init__(self, config_path: str = "config/genetic_algorithm.yaml"):
        """Initialize optimizer with configuration file"""
        self.config = self._load_config(config_path)
        
    def _load_config(self, config_path: str) -> GAConfig:
        """Load configuration from YAML file"""
        # Try to find config file in different locations
        possible_paths = [
            config_path,
            os.path.join("config", "genetic_algorithm.yaml"),
            os.path.join("..", "config", "genetic_algorithm.yaml")
        ]
        
        config_file = None
        for path in possible_paths:
            if os.path.exists(path):
                config_file = path
                break
                
        if config_file is None:
            raise FileNotFoundError(f"Configuration file not found. Tried: {possible_paths}")
            
        with open(config_file, 'r') as f:
            config_data = yaml.safe_load(f)
            
        return GAConfig(
            pop_size=config_data['population']['size'],
            hall_of_fame_size=config_data['population']['hall_of_fame_size'],
            generations=config_data['evolution']['generations'],
            crossover_prob=config_data['evolution']['crossover_probability'],
            mutation_prob=config_data['evolution']['mutation_probability'],
            gene_count=config_data['individual']['gene_count'],
            gene_min=config_data['individual']['gene_bounds']['min'],
            gene_max=config_data['individual']['gene_bounds']['max'],
            show_progress=config_data['logging']['show_progress'],
            show_statistics=config_data['logging']['show_statistics'],
            show_hall_of_fame=config_data['logging']['show_hall_of_fame']
        )
    
    def FindBestLap(self, x_s: np.ndarray, y_s: np.ndarray) -> List[LapResult]:
        """
        Find best lap using genetic algorithm
        
        Args:
            x_s: Track x coordinates (spline)
            y_s: Track y coordinates (spline)
            
        Returns:
            List of top 5 lap results from hall of fame
        """
        if self.config.show_progress:
            print(f"🏁 Starting Genetic Algorithm Optimization")
            print(f"   Population: {self.config.pop_size}")
            print(f"   Generations: {self.config.generations}")
            print(f"   Crossover: {self.config.crossover_prob}")
            print(f"   Mutation: {self.config.mutation_prob}")
            print("=" * 50)
        
        # Initialize population
        pop = toolbox.population(n=self.config.pop_size)
        
        # Setup hall of fame
        hof = tools.HallOfFame(maxsize=self.config.hall_of_fame_size)
        
        # Evaluate initial population
        for ind in pop:
            ind.fitness.values = toolbox.evaluate(ind, x_s, y_s)
            ind.generation = 0

        # Evolution loop
        for gen in range(1, self.config.generations + 1):
            # Selection
            offspring = toolbox.select(pop, len(pop))
            offspring = list(map(toolbox.clone, offspring))
            
            # Crossover
            for c1, c2 in zip(offspring[::2], offspring[1::2]):
                if random.random() < self.config.crossover_prob:
                    toolbox.mate(c1, c2)
                    del c1.fitness.values
                    del c2.fitness.values
            
            # Mutation
            for mutant in offspring:
                if random.random() < self.config.mutation_prob:
                    toolbox.mutate(mutant)
                    del mutant.fitness.values
            
            # Evaluate invalid individuals
            invalid = [ind for ind in offspring if not ind.fitness.valid]
            for ind in invalid:
                ind.fitness.values = toolbox.evaluate(ind, x_s, y_s)
            
            # Replacement
            pop[:] = offspring
            
            # Update generation
            for ind in pop:
                ind.generation = gen
                
            # Update hall of fame
            hof.update(pop)
            
            # Statistics and logging
            if self.config.show_statistics:
                fits = [ind.fitness.values[0] for ind in pop]
                best_fit = min(fits)
                avg_fit = np.mean(fits)
                print(f"Gen {gen:3d}: Best={best_fit:.2f}, Avg={avg_fit:.2f}")

        # Create results from hall of fame
        results = []
        for rank, individual in enumerate(hof, 1):
            lap_result = LapResult(
                individual=list(individual),
                lap_time=individual.fitness.values[0],
                generation=getattr(individual, 'generation', 0),
                rank=rank
            )
            results.append(lap_result)
        
        # Show hall of fame if requested
        if self.config.show_hall_of_fame:
            print("\n" + "=" * 50)
            print("🏆 HALL OF FAME - TOP 5 RESULTS")
            print("=" * 50)
            for result in results:
                print(f"#{result.rank}: {result.lap_time:.3f}s (Gen {result.generation})")
                print(f"    Individual: {[f'{x:.2f}' for x in result.individual[:5]]}...")
                print()
        
        if self.config.show_progress:
            print(f"✅ Optimization completed!")
            print(f"   Best lap time: {results[0].lap_time:.3f}s")
            print(f"   Improvement: {(20.43 - results[0].lap_time):.3f}s")
        
        return results

# Convenience function for direct usage
def FindBestLap(x_s: np.ndarray, y_s: np.ndarray, 
                config_path: str = "config/genetic_algorithm.yaml") -> List[LapResult]:
    """
    Convenience function to find best lap time
    
    Args:
        x_s: Track x coordinates (spline)
        y_s: Track y coordinates (spline) 
        config_path: Path to configuration file
        
    Returns:
        List of top 5 lap results
    """
    optimizer = GeneticOptimizer(config_path)
    return optimizer.FindBestLap(x_s, y_s)

# Example usage
if __name__ == "__main__":
    from step1_setup import x_s, y_s
    
    # Find best lap
    results = FindBestLap(x_s, y_s)
    
    # Print results
    print(f"\n🏁 OPTIMIZATION COMPLETE!")
    print(f"Best lap time: {results[0].lap_time:.3f}s")
    print(f"Best individual: {results[0].individual}") 