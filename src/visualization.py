# src/visualization.py

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from track_loader import load_waypoints, build_spline
from dynamics import (
    compute_curvature, compute_speed_limits,
    compute_segment_lengths, speed_profile_two_pass
)

def prepare_track(num_points=500):
    # Load & spline
    x, y = load_waypoints("tracks/waypoints_S.csv")
    x_s, y_s = build_spline(x, y, num_points=num_points)

    # Dynamics
    kappa    = compute_curvature(x_s, y_s)
    v_limit  = compute_speed_limits(kappa)
    ds       = compute_segment_lengths(x_s, y_s)
    v_profile = speed_profile_two_pass(v_limit, ds)

    # Compute time per segment for animation timing
    dt = ds / ( (v_profile + np.roll(v_profile, -1)) / 2 + 1e-8 )
    t_cum = np.concatenate([[0], np.cumsum(dt)])  # length num_points+1

    # Remove the duplicate last point to keep arrays same length
    t_cum = t_cum[:-1]

    return x_s, y_s, v_profile, t_cum

def animate_track(x_s, y_s, v_profile, t_cum):
    fig, ax = plt.subplots(figsize=(6,6))
    ax.plot(x_s, y_s, 'k-', lw=1, alpha=0.5)
    point, = ax.plot([], [], 'ro', ms=6)
    time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)

    ax.set_aspect('equal')
    ax.set_title("Lap Animation with Speed Profile")

    # normalize color by speed for a trailing line (optional)
    cmap = plt.get_cmap('viridis')
    norm = plt.Normalize(v_profile.min(), v_profile.max())
    for i in range(len(x_s)-1):
        ax.plot(x_s[i:i+2], y_s[i:i+2], color=cmap(norm(v_profile[i])), alpha=0.7)

    def init():
        point.set_data([], [])
        time_text.set_text('')
        return point, time_text

    def update(frame):
        # frame is an index into the spline arrays
        i = frame % len(x_s)
        point.set_data([x_s[i]], [y_s[i]])
        time_text.set_text(f"t = {t_cum[i]:.2f} s")
        return point, time_text

    # Interval between frames in ms: scale real time to animation speed
    # e.g., play 1 second of lap time in 10 seconds of animation
    total_lap_time = t_cum[-1]
    anim_duration = 10_000  # 10 seconds
    interval = anim_duration / len(x_s)

    ani = FuncAnimation(fig, update, frames=len(x_s),
                        init_func=init, blit=True, interval=interval)
    plt.show()

if __name__ == "__main__":
    x_s, y_s, v_profile, t_cum = prepare_track(num_points=500)
    animate_track(x_s, y_s, v_profile, t_cum)
