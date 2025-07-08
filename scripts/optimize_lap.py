#!/usr/bin/env python3
# scripts/optimize_lap.py
"""
Example script showing how to use the Genetic Algorithm optimizer
"""

import sys
import os
import argparse

# Add src to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from genetic_optimizer import FindBestLap, GeneticOptimizer
from track_loader import load_waypoints, build_spline
from logger_setup import setup_logger

def main():
    parser = argparse.ArgumentParser(description="Optimize lap time using Genetic Algorithm")
    parser.add_argument("--track", "-t", default="tracks/waypoints_S.csv",
                       help="Path to track waypoints CSV file")
    parser.add_argument("--config", "-c", default="config/genetic_algorithm.yaml",
                       help="Path to GA configuration file")
    parser.add_argument("--points", "-p", type=int, default=500,
                       help="Number of spline points to generate")
    parser.add_argument("--quiet", "-q", action="store_true",
                       help="Disable logging")
    
    args = parser.parse_args()
    
    # Setup logging if not quiet
    if not args.quiet:
        logger = setup_logger()
        logger.info("Starting lap time optimization")
    
    try:
        # Load track data
        print(f"📍 Loading track: {args.track}")
        x, y = load_waypoints(args.track)
        x_s, y_s = build_spline(x, y, num_points=args.points)
        print(f"   Original waypoints: {len(x)}")
        print(f"   Spline points: {len(x_s)}")
        
        # Run optimization
        print(f"⚙️  Using config: {args.config}")
        results = FindBestLap(x_s, y_s, config_path=args.config)
        
        # Display results summary
        print("\n📊 RESULTS SUMMARY")
        print("=" * 40)
        print(f"🥇 Best lap time: {results[0].lap_time:.3f}s")
        print(f"🏆 Hall of Fame size: {len(results)}")
        
        # Save best individual to file
        best_result = results[0]
        output_file = "outputs/best_individual.txt"
        os.makedirs("outputs", exist_ok=True)
        
        with open(output_file, 'w') as f:
            f.write(f"Best Lap Time: {best_result.lap_time:.6f}s\n")
            f.write(f"Generation: {best_result.generation}\n")
            f.write(f"Individual: {best_result.individual}\n")
            f.write("\nTop 5 Results:\n")
            for i, result in enumerate(results):
                f.write(f"{i+1}. {result.lap_time:.6f}s (Gen {result.generation})\n")
        
        print(f"💾 Results saved to: {output_file}")
        
        if not args.quiet:
            logger.info(f"Optimization completed. Best time: {best_result.lap_time:.3f}s")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        if not args.quiet:
            logger.error(f"Optimization failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 