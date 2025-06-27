# src/main.py
import argparse
import os
from dynamics import compute_lap_time
from track_loader import list_tracks, load_waypoints, build_spline, plot_track

def main():
    parser = argparse.ArgumentParser(
        description="Optimize lap time on a selected track"
    )
    parser.add_argument(
        "--track-location", "-t",
        type=str,
        default=None,
        help="Filename of track CSV (e.g. ../track/waypoints_S.csv)"
    )
    
    args = parser.parse_args()

    # Se não passou --track, mostra opções e sai
    if args.track_location is None:
        print(f"\nUse: python main.py --track-location ../track/waypoints_S.csv")
        return

    track_path = args.track_location
    if not os.path.isfile(track_path):
        raise FileNotFoundError(f"Track file not found: {track_path}")

    # Carrega e plota
    x, y = load_waypoints(track_path)
    x_s, y_s = build_spline(x, y)
    t0 = compute_lap_time(x_s, y_s)
    plot_track(x, y, x_s, y_s, lap_time=t0)
    print(f"Estimated lap time (s): {t0:.2f}")

if __name__ == "__main__":
    main()
