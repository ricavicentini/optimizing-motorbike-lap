# src/track_loader.py
import os
import numpy as np
from scipy.interpolate import splprep, splev
import matplotlib.pyplot as plt

def list_tracks(directory="track"):
    """Retorna a lista de arquivos .csv na pasta de tracks."""
    return [f for f in os.listdir(directory) if f.endswith(".csv")]

def load_waypoints(path):
    """Load 2D waypoints from CSV (header: x,y)."""
    data = np.loadtxt(path, delimiter=",", skiprows=1)
    return data[:,0], data[:,1]

def build_spline(x, y, num_points=500):
    tck, _ = splprep([x, y], s=0, per=True)
    u = np.linspace(0, 1, num_points)
    x_s, y_s = splev(u, tck)
    return x_s, y_s

def plot_track(x, y, x_s, y_s, lap_time=None):
    """Plot the original waypoints and the smoothed spline track."""
    plt.figure(figsize=(10, 8))
    plt.plot(x, y, 'bo-', label='Original waypoints', markersize=4)
    plt.plot(x_s, y_s, 'r-', label='Spline track', linewidth=2)
    plt.axis('equal')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Add lap time to title if provided
    if lap_time is not None:
        plt.title(f'Track Layout - Estimated Lap Time: {lap_time:.2f}s')
    else:
        plt.title('Track Layout')
    
    plt.xlabel('X coordinate')
    plt.ylabel('Y coordinate')
    
    # Add lap time as text on the plot
    if lap_time is not None:
        plt.text(0.02, 0.98, f'Lap Time: {lap_time:.2f}s', 
                transform=plt.gca().transAxes, 
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
                verticalalignment='top', fontsize=12, fontweight='bold')
    
    plt.show()
