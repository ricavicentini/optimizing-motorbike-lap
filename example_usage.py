#!/usr/bin/env python3
# example_usage.py
"""
Simple example of how to use the new genetic optimizer
"""

import sys
import os
sys.path.append('src')

def example_basic_usage():
    """Basic usage example"""
    print("🧬 GENETIC ALGORITHM OPTIMIZATION EXAMPLE")
    print("=" * 50)
    
    try:
        # Import required modules
        from genetic_optimizer import FindBestLap
        from track_loader import load_waypoints, build_spline
        
        # Load track data
        print("📍 Loading track data...")
        x, y = load_waypoints("tracks/waypoints_S.csv")
        x_s, y_s = build_spline(x, y, num_points=500)
        
        # Run optimization with default config
        print("\n🚀 Starting optimization...")
        results = FindBestLap(x_s, y_s)
        
        # Display results
        print(f"\n✅ OPTIMIZATION COMPLETE!")
        print(f"🥇 Best lap time: {results[0].lap_time:.3f}s")
        print(f"🏆 Top 5 results:")
        for i, result in enumerate(results):
            print(f"   #{i+1}: {result.lap_time:.3f}s (Gen {result.generation})")
            
        return results
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("📦 You may need to update your conda environment:")
        print("   conda env update -f environment.yml")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def example_custom_config():
    """Example with custom configuration"""
    print("\n🔧 CUSTOM CONFIGURATION EXAMPLE")
    print("=" * 50)
    
    try:
        from genetic_optimizer import GeneticOptimizer
        from track_loader import load_waypoints, build_spline
        
        # Create custom config (you can modify config/genetic_algorithm.yaml)
        print("⚙️  Using custom configuration...")
        
        # Load track
        x, y = load_waypoints("tracks/waypoints_S.csv")
        x_s, y_s = build_spline(x, y, num_points=300)  # Fewer points for faster execution
        
        # Create optimizer instance
        optimizer = GeneticOptimizer("config/genetic_algorithm.yaml")
        
        # Run optimization
        results = optimizer.FindBestLap(x_s, y_s)
        
        print(f"🎯 Custom optimization complete!")
        print(f"   Best time: {results[0].lap_time:.3f}s")
        
        return results
        
    except Exception as e:
        print(f"❌ Custom config error: {e}")
        return None

if __name__ == "__main__":
    # Check if config directory exists
    if not os.path.exists("config"):
        print("⚠️  Config directory not found. Creating it...")
        os.makedirs("config", exist_ok=True)
    
    # Check if PyYAML is available
    try:
        import yaml
        print("✅ PyYAML is installed")
    except ImportError:
        print("❌ PyYAML not found. Update environment with:")
        print("   conda env update -f environment.yml")
        sys.exit(1)
    
    # Run examples
    print("Running basic optimization example...")
    basic_results = example_basic_usage()
    
    if basic_results:
        print("\nRunning custom configuration example...")
        custom_results = example_custom_config()
        
        if custom_results:
            print(f"\n🏁 COMPARISON:")
            print(f"   Basic: {basic_results[0].lap_time:.3f}s")
            print(f"   Custom: {custom_results[0].lap_time:.3f}s")
    
    print("\n✨ Example completed!") 