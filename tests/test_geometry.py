"""Tests für geometry.py: die Beispiele aus der Vorlesung, in der Reihenfolge der Folien.

Zwei Tests schlagen absichtlich fehl, test_find_intersection_rejects_mismatched_lengths und test_1. Der Grund ist ein
echter Fehler: find_intersection() prüft nicht, ob x_road und y_road gleich lang sind.
"""

import numpy as np
import pytest

from road_profile_viewer.geometry import find_intersection

# Die Straße für alle Tests ohne eigene Straße. Auf den Folien ist sie nicht zu sehen.
x_road = np.array([0, 10, 20, 30], dtype=np.float64)
y_road = np.array([0, 2, 4, 6], dtype=np.float64)


# Folie „Beispiel Unit-Test“
def test_find_intersection_normal_angle():
    """Test that find_intersection() works with a normal downward angle."""
    # Arrange: Set up test data
    x_road = np.array([0, 10, 20, 30])
    y_road = np.array([0, 2, 3, 4])
    angle = 10.0  # positive angle = downward ray

    # Act: Call the function
    x, y, dist = find_intersection(x_road, y_road, angle)

    # Assert: Verify the result
    assert x is not None, "Should find an intersection"
    assert dist > 0, "Distance should be positive"


# Folie „Ihr erster Unit-Test“. Die Folie „AAA-Pattern in der Praxis“ zeigt denselben Test ausführlicher,
# mit den Variablen angle, camera_x, camera_y und einem dritten assert (0 <= x <= 30).
def test_find_intersection_finds_intersection_for_normal_angle():
    # Arrange
    x_road = np.array([0, 10, 20, 30], dtype=np.float64)
    y_road = np.array([0, 2, 4, 6], dtype=np.float64)
    # Act
    x, y, dist = find_intersection(x_road, y_road, 10.0, 0.0, 10.0)
    # Assert
    assert x is not None
    assert dist > 0


# Folie „pytest Output Beispiel“: die fünf Tests aus der Ausgabe.
# Die Docstrings stammen von der Folie „Beschreibende Testnamen: Gute Beispiele“.
def test_find_intersection_finds_intersection_for_downward_angle():
    """Sie wissen genau, was das testet"""
    x, y, dist = find_intersection(x_road, y_road, 10.0, 0.0, 10.0)
    assert x is not None


def test_find_intersection_returns_none_for_vertical_angle():
    """Klares Ergebnis für den Randfall"""
    x, y, dist = find_intersection(x_road, y_road, 90.0)
    assert x is None


def test_find_intersection_returns_none_for_empty_arrays():
    """Klar: Funktion + Szenario + erwartetes Ergebnis"""
    x, y, dist = find_intersection(np.array([]), np.array([]), 10.0)
    assert x is None


def test_find_intersection_rejects_mismatched_lengths():
    x_road = np.array([0.0, 10.0, 20.0, 30.0])
    y_road = np.array([0.0, 2.0, 4.0])  # ein Wert fehlt

    # pytest.raises erwartet einen ValueError, also eine klare Fehlermeldung.
    # find_intersection() wirft aber einen IndexError, deshalb ist der Test rot.
    with pytest.raises(ValueError):
        find_intersection(x_road, y_road, 10.0, 0.0, 10.0)


def test_find_intersection_returns_none_when_ray_misses_road():
    """Szenario und Ergebnis sind explizit"""
    x, y, dist = find_intersection(x_road, y_road, -10.0, 0.0, 10.0)  # Strahl nach oben
    assert x is None


# Folie „Prinzip 1: Ein Konzept pro Test“. Schlecht: mehrere Konzepte in einem einzigen Test
def test_find_intersection_everything():
    x, y, dist = find_intersection(x_road, y_road, 10.0, 0.0, 10.0)
    assert x is not None  # Konzept 1: Strahl nach unten

    x2, y2, dist2 = find_intersection(x_road, y_road, 90.0)
    assert x2 is None  # Konzept 2: senkrechter Strahl

    x3, y3, dist3 = find_intersection(np.array([]), np.array([]), 10.0)
    assert x3 is None  # Konzept 3: leere Arrays


# Folie „Ein Konzept pro Test: Gutes Beispiel“. Gut: drei separate Tests, jeder mit genau einem Konzept.
# Die beiden anderen stehen weiter oben bei „pytest Output Beispiel“.
def test_find_intersection_returns_intersection_for_downward_angle():
    x, y, dist = find_intersection(x_road, y_road, 10.0, 0.0, 10.0)
    assert x is not None


# Folie „Prinzip 2: Ein Assert pro Test“. Ideal: ein Assert
def test_find_intersection_returns_positive_distance():
    """Test that distance is positive when an intersection is found."""
    x_road = np.array([0, 10, 20, 30], dtype=np.float64)
    y_road = np.array([0, 2, 4, 6], dtype=np.float64)
    x, y, dist = find_intersection(x_road, y_road, 10.0, 0.0, 10.0)
    assert dist > 0  # Ein Konzept: Distanz ist positiv


# Folie „Wann mehrere Asserts OK sind“. OK: mehrere Asserts, aber alle prüfen dasselbe Konzept
def test_find_intersection_returns_valid_coordinates():
    x_road = np.array([0, 10, 20, 30], dtype=np.float64)
    y_road = np.array([0, 2, 4, 6], dtype=np.float64)
    x, y, dist = find_intersection(x_road, y_road, 10.0, 0.0, 10.0)

    # Alle prüfen DASSELBE Konzept: gültige Koordinaten
    assert x is not None
    assert y is not None
    assert 0 <= x <= 30
    assert 0 <= y <= 6


# Folie „Wann Tests aufteilen“. Schlecht: zwei verschiedene Konzepte in einem Test
def test_find_intersection_coordinates_and_distance():
    x, y, dist = find_intersection(x_road, y_road, 10.0, 0.0, 10.0)
    assert x > 0  # Konzept 1
    assert dist > 0  # Konzept 2


# Gut: ein Test pro Konzept. Der zweite steht weiter oben: test_find_intersection_returns_positive_distance
def test_find_intersection_returns_positive_x():
    x, y, dist = find_intersection(x_road, y_road, 10.0, 0.0, 10.0)
    assert x > 0


# Folie „Prinzip 3: Beschreibende Testnamen“. Schlecht: Die Namen sagen nicht, was getestet wird.
# test_1 prüft dasselbe wie test_find_intersection_rejects_mismatched_lengths und schlägt genauso fehl. Vergleichen
# Sie die beiden FAILED-Zeilen am Ende von uv run pytest (Folie „Warum beschreibende Namen wichtig sind“).
def test_1():  # Was testet das?
    with pytest.raises(ValueError):
        find_intersection(x_road, np.array([0.0, 2.0, 4.0]), 10.0, 0.0, 10.0)


def test_intersection():  # Zu vage
    x, y, dist = find_intersection(x_road, y_road, 10.0, 0.0, 10.0)
    assert x is not None


def test_angle():  # Welcher Winkel? Was ist damit?
    x, y, dist = find_intersection(x_road, y_road, 90.0)
    assert x is None


def test_edge_case():  # Welcher Randfall?
    x, y, dist = find_intersection(np.array([]), np.array([]), 10.0)
    assert x is None
