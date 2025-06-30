import numpy as np

def log_waypoints(x, y, title="ORIGINAL WAYPOINTS", logger=None):
    """Log all waypoints to terminal in a formatted table."""
    lines = []
    lines.append(f"=== {title} ===")
    lines.append(f"Total waypoints: {len(x)}")
    lines.append("Index | X coord | Y coord")
    lines.append("-" * 30)
    
    for i, (x_val, y_val) in enumerate(zip(x, y)):
        lines.append(f"{i:5d} | {x_val:7.2f} | {y_val:7.2f}")
    
    lines.append("=" * 30)
    
    # Always print to console
    for line in lines:
        print(line)
    
    # Also log to file if logger provided
    if logger:
        logger.info(f"Loaded {len(x)} waypoints for track analysis")

def log_spline_info(x_s, y_s, num_preview=5, logger=None):
    """Log spline interpolation information."""
    lines = []
    lines.append(f"=== SPLINE INTERPOLATION ===")
    lines.append(f"Spline points generated: {len(x_s)}")
    lines.append(f"First {num_preview} spline points:")
    
    for i in range(min(num_preview, len(x_s))):
        lines.append(f"  {i}: ({x_s[i]:.2f}, {y_s[i]:.2f})")
    
    lines.append("=" * 30)
    
    # Always print to console
    for line in lines:
        print(line)
    
    # Also log to file if logger provided
    if logger:
        logger.info(f"Generated {len(x_s)} spline points from original waypoints")

def log_dynamics_info(v_profile, t_cum, kappa=None, logger=None):
    """Log dynamics simulation information."""
    lines = []
    lines.append(f"=== DYNAMICS SIMULATION ===")
    lines.append(f"Speed profile computed for {len(v_profile)} segments")
    lines.append(f"Total lap time: {t_cum[-1]:.2f} seconds")
    lines.append(f"Max speed: {np.max(v_profile)*3.6:.1f} km/h")
    lines.append(f"Min speed: {np.min(v_profile)*3.6:.1f} km/h")
    lines.append(f"Average speed: {np.mean(v_profile)*3.6:.1f} km/h")
    
    if kappa is not None:
        lines.append(f"Max curvature: {np.max(np.abs(kappa)):.4f} rad/m")
        lines.append(f"Sharpest turn radius: {1/(np.max(np.abs(kappa)) + 1e-8):.1f} m")
    
    lines.append("=" * 30)
    
    # Always print to console
    for line in lines:
        print(line)
    
    # Also log to file if logger provided
    if logger:
        logger.info(f"Dynamics simulation completed - Lap time: {t_cum[-1]:.2f}s, Max speed: {np.max(v_profile)*3.6:.1f} km/h")

def log_track_summary(x, y, x_s, y_s, v_profile, t_cum, logger=None):
    """Log comprehensive track analysis summary."""
    track_length = np.sum(np.sqrt(np.diff(x_s)**2 + np.diff(y_s)**2))
    
    lines = []
    lines.append(f"=== TRACK SUMMARY ===")
    lines.append(f"Original waypoints: {len(x)}")
    lines.append(f"Interpolated points: {len(x_s)}")
    lines.append(f"Track length: {track_length:.1f} meters")
    lines.append(f"Estimated lap time: {t_cum[-1]:.2f} seconds")
    lines.append(f"Average lap speed: {track_length/t_cum[-1]*3.6:.1f} km/h")
    lines.append("=" * 30)
    
    # Always print to console
    for line in lines:
        print(line)
    
    # Also log to file if logger provided
    if logger:
        logger.info(f"Track analysis complete - Length: {track_length:.1f}m, Time: {t_cum[-1]:.2f}s, Avg speed: {track_length/t_cum[-1]*3.6:.1f} km/h") 