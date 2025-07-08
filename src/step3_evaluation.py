# step3_evaluation.py

import numpy as np
from dynamics import compute_lap_time

def evaluate(individual, x_s, y_s):
    """
    1) Recebe individual de tamanho 10
    2) Interpola para 100 pontos
    3) Desenha nova trajectória e chama compute_lap_time
    """
    # 1) Cria parâmetro u para 10 e para 100
    u10 = np.linspace(0, 1, len(individual))
    u100 = np.linspace(0, 1, len(x_s))

    # 2) Interpola offsets para cada ponto spline
    offsets = np.interp(u100, u10, individual)

    # 3) Calcula normais à centerline
    dx = np.gradient(x_s)
    dy = np.gradient(y_s)
    norms = np.hypot(dx, dy)
    nx = -dy / norms
    ny =  dx / norms

    # 4) Desloca centerline
    x_traj = x_s + offsets * nx
    y_traj = y_s + offsets * ny

    # 5) Calcula tempo de volta
    t = compute_lap_time(x_traj, y_traj)
    return (t,)
