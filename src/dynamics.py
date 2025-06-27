# src/dynamics.py

import numpy as np

def compute_curvature(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """
    Estimate curvature κ at each point of a closed spline.
    Uses finite differences on a periodic curve.
    """
    # First derivatives
    dx = np.gradient(x)
    dy = np.gradient(y)
    # Second derivatives
    ddx = np.gradient(dx)
    ddy = np.gradient(dy)
    # Curvature formula: |x'y'' - y'x''| / (x'^2 + y'^2)^(3/2)
    num = np.abs(dx * ddy - dy * ddx)
    den = (dx**2 + dy**2)**1.5
    # avoid division by zero
    curvature = num / np.maximum(den, 1e-8)
    return curvature

def compute_speed_limits(curvature: np.ndarray,
                         mu: float = 1.1,
                         g: float = 9.81) -> np.ndarray:
    """
    Given curvature array, compute the max cornering speed:
       v_max = sqrt(mu * g / κ)
    For κ=0 (straight), we set a high cap.
    """
    v_max = np.sqrt(mu * g / np.maximum(curvature, 1e-8))
    return v_max

def compute_segment_lengths(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """
    Compute Euclidean distance between successive points,
    assuming closed-loop (last→first).
    """
    dx = np.diff(x, append=x[0])
    dy = np.diff(y, append=y[0])
    return np.hypot(dx, dy)

def speed_profile_two_pass(v_limit: np.ndarray,
                           ds: np.ndarray,
                           a_max: float = 2.5,
                           a_min: float = -5.0) -> np.ndarray:
    """
    Build a velocity profile along the track:
      1. Forward pass (acceleration limit)
      2. Backward pass (braking limit)
    Returns v[i] at each node.
    """
    n = len(v_limit)
    v = v_limit.copy()
    # Forward pass: acceleration
    for i in range(1, n):
        v_prev = v[i-1]
        v[i] = min(v[i], np.sqrt(v_prev**2 + 2*a_max*ds[i-1]))
    # Backward pass: braking
    for i in range(n-2, -1, -1):
        v_next = v[i+1]
        v[i] = min(v[i], np.sqrt(v_next**2 + 2*abs(a_min)*ds[i]))
    # ensure closure: last vs first
    v[0] = v[-1] = min(v[0], v[-1])
    return v

def compute_lap_time(x: np.ndarray,
                     y: np.ndarray,
                     mu: float = 1.1,
                     g: float = 9.81,
                     a_max: float = 2.5,
                     a_min: float = -5.0) -> float:
    """
    Full lap-time estimation:
      1. curvature → v_limit
      2. segment lengths ds
      3. two-pass speed profile
      4. trapezoidal integration of time: sum(ds / v_avg)
    """
    curvature = compute_curvature(x, y)
    v_limit = compute_speed_limits(curvature, mu, g)
    ds = compute_segment_lengths(x, y)
    v_profile = speed_profile_two_pass(v_limit, ds, a_max, a_min)
    # time per segment: ds / v_avg between nodes
    v_next = np.roll(v_profile, -1)
    time_segments = ds / ((v_profile + v_next) / 2 + 1e-8)
    return np.sum(time_segments)

# Quick self-test
if __name__ == "__main__":
    from track_loader import load_waypoints, build_spline
    # load & spline
    x, y = load_waypoints("tracks/waypoints_S.csv")
    x_s, y_s = build_spline(x, y, num_points=500)
    t0 = compute_lap_time(x_s, y_s)
    print(f"Estimated lap time (s): {t0:.2f}")
