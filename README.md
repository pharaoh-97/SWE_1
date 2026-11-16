# Road Profile Viewer: Testen mit pytest

Der Ausgangspunkt für das Kapitel Testen. Das Repo enthält den Road Profile Viewer nach dem Refactoring: vier Module
statt einer großen `main.py`, ruff und pyright ohne Befund. **pytest ist eingerichtet**, und `tests/test_geometry.py`
enthält die Tests aus der Vorlesung.

## Was drin ist

```text
src/road_profile_viewer/
├── __init__.py        lädt bewusst nichts, damit Tests von geometry.py kein Dash brauchen
├── geometry.py        Mathematik: Kamerastrahl und Schnittpunkt mit der Straße
├── road.py            Straßenprofil erzeugen
├── visualization.py   Dash-Oberfläche
└── main.py            Einstieg: App bauen und starten
tests/
├── __init__.py
└── test_geometry.py   Tests für geometry.py, in der Reihenfolge der Folien
messdaten.py           Skript der Folie „Die schockierende Entdeckung“
manual_test.py         Skript der Folie „Test-Frameworks: Warum wir pytest brauchen“
pyproject.toml         Abhängigkeiten und Einstellungen für ruff, pyright und pytest
```

## Einrichten

Sie brauchen einen GitHub-Account, git, uv und einen Editor (z. B. VS Code).

1. **Eigenes Repo anlegen:** Öffnen Sie
   <https://github.com/hs-aalen-software-engineering/road-profile-viewer-testing-template> und klicken Sie oben rechts
   auf **Use this template → Create a new repository**. Owner ist Ihr Account, der Name ist frei wählbar. Dann
   **Create repository**.
2. **Klonen und starten:**

   ```bash
   git clone https://github.com/<account>/<repo-name>.git
   cd <repo-name>
   uv sync
   uv run road-profile-viewer
   ```

   Öffnen Sie im Browser <http://127.0.0.1:8050/>. Neben dem Winkel-Feld steht in Rot:

   ```text
   Intersection found at (74.23, 3.43) | Distance: 74.24 units
   ```

   Beenden Sie den Server mit Strg+C.
3. **Startzustand prüfen:**

   ```bash
   uv run ruff check
   uv run ruff format --check
   uv run pyright
   uv run pytest
   ```

   Erwartet: `All checks passed!`, `9 files already formatted` und `0 errors, 0 warnings, 0 informations`. pytest
   meldet am Ende `2 failed, 15 passed`. Die beiden roten Tests sind Absicht, siehe
   [Zwei bekannte Fehler](#zwei-bekannte-fehler-in-find_intersection).

## Die Tests aus der Vorlesung

`tests/test_geometry.py` enthält die Tests von den Folien, in derselben Reihenfolge. Vor den Tests jeder Folie steht
deren Titel als Kommentar. Zeigen mehrere Folien denselben Test, steht er nur einmal in der Datei. Die Schritte der
Folie „Ihren ersten Unit-Test schreiben“ sind hier schon erledigt: pytest ist installiert, und `tests/` gibt es bereits.

- **Alle Tests:** `uv run pytest`. Mit `-v` erscheint jeder Test einzeln, mit `-x` stoppt pytest beim ersten Fehler,
  mit `-k "intersection"` laufen nur Tests mit „intersection“ im Namen.
- **Genau die fünf Tests der Folie „pytest Output Beispiel“:**

  ```bash
  uv run pytest tests/test_geometry.py -v -k "finds_intersection_for_downward or vertical or empty or mismatched or misses"
  ```

  Am Ende meldet pytest zusätzlich `12 deselected`, das sind die übrigen Tests der Datei.
- **Nur Ihr erster Unit-Test** (Folien „Ihr erster Unit-Test“ und „Ihren ersten Test ausführen“):

  ```bash
  uv run pytest tests/test_geometry.py::test_find_intersection_finds_intersection_for_normal_angle -v
  ```

- **Schlechter gegen guten Testnamen** (Folie „Warum beschreibende Namen wichtig sind“): `test_1` und
  `test_find_intersection_rejects_mismatched_lengths` prüfen dasselbe und schlagen beide fehl. Vergleichen Sie die
  beiden `FAILED`-Zeilen am Ende von `uv run pytest`.
- **Kürzere Fehlerausgabe:** Mit `--tb=short` zeigt pytest pro Fehler nur die wichtigsten Zeilen.

## Die zwei Skripte

- `uv run python messdaten.py` bricht mit `IndexError: index 3 is out of bounds for axis 0 with size 3` ab, wie auf der
  Folie „Die schockierende Entdeckung“.
- `uv run python manual_test.py` meldet `PASSED`. Ändern Sie im Aufruf `find_intersection(x_road, y_road, 10.0)` den
  Winkel `10.0` in `-10.0` (Strahl nach oben): Das Skript meldet `FAILED`, endet aber trotzdem mit Exit-Code 0, eine CI
  bliebe also grün. Den Exit-Code zeigt danach `echo $?` (bash, zsh) bzw. `$LASTEXITCODE` (PowerShell). pytest endet
  bei einem roten Test mit Exit-Code 1.

## Zwei bekannte Fehler in find_intersection()

Weder ruff noch pyright findet sie. Die Fehler bleiben vorerst im Code, denn die Beispiele bauen darauf auf.

1. **Arrays ungleich lang:** Ist `y_road` kürzer als `x_road`, bricht die Funktion je nach Winkel mit einem
   `IndexError` ab, statt klar zu melden, was falsch ist. Bei anderen Winkeln fällt der fehlende Wert gar nicht auf.
   Daran scheitern `test_find_intersection_rejects_mismatched_lengths` und `test_1`.
2. **Punkt hinter der Kamera:** Steht die Kamera zwischen zwei Straßenpunkten über einer steil fallenden Straße, kann
   die Funktion einen Schnittpunkt hinter der Kamera liefern. Beispiel: Kamera bei (5, 3), die Straße fällt von (0, 5)
   nach (10, 0) und bleibt dann flach bis (30, 0), Winkel 10°. Die Funktion liefert (3.46, 3.27), richtig wäre
   (22.01, 0.00).
