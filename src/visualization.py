# src/visualization.py

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from track_loader import load_waypoints, build_spline
from dynamics import (
    compute_curvature, compute_speed_limits,
    compute_segment_lengths, speed_profile_two_pass
)
from logger import log_waypoints, log_spline_info, log_dynamics_info, log_track_summary

def prepare_track(num_points=500):
    # 1) Load & spline
    x, y = load_waypoints("tracks/waypoints_S.csv")
    log_waypoints(x, y)
    
    x_s, y_s = build_spline(x, y, num_points=num_points)
    log_spline_info(x_s, y_s)

    # 2) Dynamics
    kappa    = compute_curvature(x_s, y_s)
    v_limit  = compute_speed_limits(kappa)
    ds       = compute_segment_lengths(x_s, y_s)
    v_profile = speed_profile_two_pass(v_limit, ds)

    # 3) Time per segment and cumulative time
    dt = ds / ( (v_profile + np.roll(v_profile, -1)) / 2 + 1e-8 )
    t_cum = np.concatenate([[0], np.cumsum(dt)])  # length num_points+1
    t_cum = t_cum[:-1]  # Remove duplicate last point to match array lengths

    # 4) Approximate longitudinal acceleration a = dv/dt
    # note: dv between i and i-1 over dt[i-1]
    dv    = np.diff(v_profile, prepend=v_profile[-1])
    a_long = dv / np.concatenate([[dt[-1]], dt[:-1]])
    
    # Log dynamics and track summary
    log_dynamics_info(v_profile, t_cum, kappa)
    log_track_summary(x, y, x_s, y_s, v_profile, t_cum)

    return x_s, y_s, v_profile, a_long, kappa, t_cum

def animate_track(x_s, y_s, v, a, kappa, t_cum):
    fig, ax = plt.subplots(figsize=(8,8))
    ax.plot(x_s, y_s, 'k-', lw=1, alpha=0.5)
    
    bike, = ax.plot([], [], 'ro', ms=8)
    
    # HUD text using ax.text (works better with blitting)
    speed_text     = ax.text(0.02, 0.98, '', transform=ax.transAxes, fontsize=12, 
                            color='white', bbox=dict(facecolor='black', alpha=0.8))
    accel_text     = ax.text(0.02, 0.93, '', transform=ax.transAxes, fontsize=12, 
                            color='white', bbox=dict(facecolor='black', alpha=0.8))
    curvature_text = ax.text(0.02, 0.88, '', transform=ax.transAxes, fontsize=12, 
                            color='white', bbox=dict(facecolor='black', alpha=0.8))
    lap_time_text  = ax.text(0.70, 0.98, '', transform=ax.transAxes, fontsize=14, 
                            color='yellow', bbox=dict(facecolor='black', alpha=0.8))
    
    ax.set_aspect('equal')
    ax.set_facecolor('#333333')            # dark background
    ax.set_title("Lap Animation with HUD", color='white', fontsize=16)
    ax.tick_params(colors='white')         # white tick labels
    ax.spines['bottom'].set_color('white')
    ax.spines['top'].set_color('white')
    ax.spines['right'].set_color('white')
    ax.spines['left'].set_color('white')

    # Pre-plot colored trail by speed
    cmap = plt.get_cmap('viridis')
    norm = plt.Normalize(v.min(), v.max())
    for i in range(len(x_s)-1):
        ax.plot(x_s[i:i+2], y_s[i:i+2],
                color=cmap(norm(v[i])),
                alpha=0.6, lw=3)

    def init():
        bike.set_data([], [])
        speed_text.set_text('')
        accel_text.set_text('')
        curvature_text.set_text('')
        lap_time_text.set_text('')
        return bike, speed_text, accel_text, curvature_text, lap_time_text

    def update(frame):
        # frame is an index into the spline arrays
        i = frame % len(x_s)
        bike.set_data([x_s[i]], [y_s[i]])
        speed_text.set_text(f"Speed: {v[i]:.1f} m/s")
        accel_text.set_text(f"Accel: {a[i]:+.2f} m/s²")
        curvature_text.set_text(f"Curv: {kappa[i]:.3f} 1/m")
        lap_time_text.set_text(f"Lap time: {t_cum[i]:.2f} s")
        return bike, speed_text, accel_text, curvature_text, lap_time_text

    # animation speed: map real lap to ~15s of playback
    total_time   = t_cum[-1]
    playback_sec = 15_000  # milliseconds
    interval     = playback_sec / len(x_s)

    ani = FuncAnimation(fig, update, frames=len(x_s),
                        init_func=init, blit=False, interval=interval)
    plt.show()

if __name__ == "__main__":
    x_s, y_s, v_profile, a_long, kappa, t_cum = prepare_track(num_points=500)
    animate_track(x_s, y_s, v_profile, a_long, kappa, t_cum)
