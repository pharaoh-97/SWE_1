# Folie „Die schockierende Entdeckung“
# Starten mit: uv run python messdaten.py

import numpy as np

from road_profile_viewer.geometry import find_intersection

x_road = np.array([0.0, 10.0, 20.0, 30.0])
y_road = np.array([0.0, 2.0, 4.0])  # ein Wert fehlt

find_intersection(x_road, y_road, 10.0, 0.0, 10.0)
