# src/logger.py

import numpy as np

def log_waypoints(x, y, title="ORIGINAL WAYPOINTS"):
    """Log all waypoints to terminal in a formatted table."""
    print(f"=== {title} ===")
    print(f"Total waypoints: {len(x)}")
    print("Index | X coord | Y coord")
    print("-" * 30)
    
    for i, (x_val, y_val) in enumerate(zip(x, y)):
        print(f"{i:5d} | {x_val:7.2f} | {y_val:7.2f}")
    
    print("=" * 30)

def log_spline_info(x_s, y_s, num_preview=5):
    """Log spline interpolation information."""
    print(f"\n=== SPLINE INTERPOLATION ===")
    print(f"Spline points generated: {len(x_s)}")
    print(f"First {num_preview} spline points:")
    
    for i in range(min(num_preview, len(x_s))):
        print(f"  {i}: ({x_s[i]:.2f}, {y_s[i]:.2f})")
    
    print("=" * 30)

def log_dynamics_info(v_profile, t_cum, kappa=None):
    """Log dynamics simulation information."""
    print(f"\n=== DYNAMICS SIMULATION ===")
    print(f"Speed profile computed for {len(v_profile)} segments")
    print(f"Total lap time: {t_cum[-1]:.2f} seconds")
    print(f"Max speed: {np.max(v_profile):.1f} m/s")
    print(f"Min speed: {np.min(v_profile):.1f} m/s")
    print(f"Average speed: {np.mean(v_profile):.1f} m/s")
    
    if kappa is not None:
        print(f"Max curvature: {np.max(np.abs(kappa)):.4f} rad/m")
        print(f"Sharpest turn radius: {1/(np.max(np.abs(kappa)) + 1e-8):.1f} m")
    
    print("=" * 30)

def log_track_summary(x, y, x_s, y_s, v_profile, t_cum):
    """Log comprehensive track analysis summary."""
    track_length = np.sum(np.sqrt(np.diff(x_s)**2 + np.diff(y_s)**2))
    
    print(f"\n=== TRACK SUMMARY ===")
    print(f"Original waypoints: {len(x)}")
    print(f"Interpolated points: {len(x_s)}")
    print(f"Track length: {track_length:.1f} meters")
    print(f"Estimated lap time: {t_cum[-1]:.2f} seconds")
    print(f"Average lap speed: {track_length/t_cum[-1]*3.6:.1f} km/h")
    print("=" * 30) 