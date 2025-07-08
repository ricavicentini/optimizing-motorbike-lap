# step1_setup.py

import numpy as np
from deap import base, creator, tools
from track_loader import load_waypoints, build_spline
from dynamics import compute_lap_time

# Carrega uma spline de 100 pontos (simplificamos para ficar rápido)
x_wp, y_wp = load_waypoints("tracks/waypoints_S.csv")
x_s, y_s = build_spline(x_wp, y_wp, num_points=100)
