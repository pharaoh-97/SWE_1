# Folie „Test-Frameworks: Warum wir pytest brauchen“
# Starten mit: uv run python manual_test.py

import numpy as np

from road_profile_viewer.geometry import find_intersection

x_road = np.array([0.0, 10.0, 20.0, 30.0])
y_road = np.array([0.0, 2.0, 4.0, 6.0])


# Ohne Test-Framework:
def manual_test():
    x, y, dist = find_intersection(x_road, y_road, 10.0)
    if x is None:
        print("FAILED: x should not be None")
        return False
    if dist <= 0:
        print("FAILED: distance should be positive")
        return False
    print("PASSED")
    return True


# Test manuell ausführen
manual_test()
