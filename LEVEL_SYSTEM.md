# Level System

Dieses Platformer-Spiel verwendet ein Level-System mit `.map` Dateien.

## Level-Dateien

Alle Level werden in Dateien mit der Erweiterung `.map` gespeichert. Diese befinden sich im gleichen Verzeichnis wie `platformer.py`.

### Verfügbare Level

- `default.map` - Das Standard-Level mit verschiedenen Schwierigkeitsgraden
- `easy.map` - Ein einfacheres Level mit einer Treppenstruktur

## Neue Level erstellen

### Methode 1: JSON-Format (Empfohlen)

Erstelle eine neue Datei mit der Erweiterung `.map`, z.B. `my_level.map`:

```json
[
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [2, 2, 0, 0, 0, 0, 0, 0, 3, 0],
  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]
```

### Tile-Typen

Die Zahlen in der Level-Array bedeuten:

| Zahl | Bedeutung | Beschreibung |
|------|-----------|------------|
| 0 | Leer | Leerer Platz |
| 1 | Dirt | Schmutzblock (solide) |
| 2 | Grass | Grasblock (Plattform) |
| 3 | Enemy | Gegner/Blob |
| 4 | Coin | Multivitaminsaft zum Sammeln |
| 5 | Coin | Multivitaminsaft zum Sammeln |
| 6 | Lava | Lava (tödlich) |
| 8 | Spezial | Spezial-Element |

### Level-Namen

Der Name des Levels wird automatisch aus dem Dateinamen generiert:
- `default.map` → "default"
- `my_custom_level.map` → "my_custom_level"

## Spiel starten

Wenn Sie das Spiel starten:

1. **Level-Auswahl Dialog** erscheint in einem Pygame-Fenster
2. **Navigation:**
   - **Zahltasten (1-9)**: Direkt ein Level auswählen
   - **Pfeiltasten (↑/↓)**: Zwischen Leveln navigieren
   - **Enter/Space**: Ausgewähltes Level bestätigen
   - **Maus**: Auf einen Level-Button klicken zum Auswählen
3. Das ausgewählte Level wird geladen
4. Der Fenstertitel zeigt z.B. "Platformer - Level: default"

Das Auswahl-Dialog bietet eine intuitive grafische Oberfläche mit:
- Markierung des aktuell ausgewählten Levels (gelber Hintergrund)
- Visuelle Buttons für jedes Level
- Hilfsmeldung mit Kontrollanleitung

## Level Manager API

Die `level_manager.py` Datei bietet folgende Funktionen:

```python
from level_manager import *

# Alle .map Dateien finden
map_files = get_map_files()

# Ein Level laden
world_data = load_level('path/to/level.map')

# Ein Level speichern
save_level(world_data, 'path/to/new_level.map')

# Freundlichen Namen aus Datei extrahieren
name = get_level_name('default.map')  # Returns: "default"
```

## Tipps zum Level-Design

- **Breite**: Die Level sollten mindestens 30-40 Tiles breit sein für interessantes Gameplay
- **Höhe**: 15-20 Tiles sind eine gute Höhe
- **Startposition**: Der Spieler startet auf der linken Seite (x=50)
- **Schwierigkeit**: Verwenden Sie Feinde und Lava strategisch
- **Plattformen**: Gras (2) ist am besten für Plattformen

## Fehlerbehandlung

Wenn keine `.map` Dateien gefunden werden, wird das Programm mit einer Fehlermeldung beendet. Stellen Sie sicher, dass mindestens eine `.map` Datei im Spieleverzeichnis existiert.
