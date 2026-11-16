"""Road Profile Viewer.

The application is split into focused modules:

- geometry.py: camera ray and its intersection with the road
- road.py: road profile generation
- visualization.py: Dash user interface
- main.py: entry point that builds and starts the app

This file deliberately imports nothing. Importing road_profile_viewer.geometry
(for example in a unit test) therefore does not load Dash.
"""

__version__ = "0.1.0"
