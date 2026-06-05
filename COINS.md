# Coin System - Multivitaminsaft

Das Spiel verfügt jetzt über ein Coin-Sammelsystem mit **Multivitaminsaft-Objekten**.

## Gameplay

- Der Spieler **sammelt Multivitaminsäfte** ein, indem er sie berührt
- Jeder Coin wird durch das Bild `res/multivitaminsaft.png` dargestellt
- Der **Coin-Zähler** wird oben links im Spiel angezeigt
- Format: `Coins: X/Y` (gesammelt/gesamt)

## Level-Design

### Coins hinzufügen

Um Coins in einem Level zu platzieren, verwende den Tile-Wert **4** oder **5** in deiner `.map` Datei:

```json
[
  [0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0],
  [0, 4, 0, 4, 0, 4, 0, 0],
  [2, 2, 2, 2, 2, 2, 2, 2],
  [1, 1, 1, 1, 1, 1, 1, 1]
]
```

### Verfügbare Level mit Coins

- **default.map**: 8 Coins
- **easy.map**: 12 Coins

## Technische Details

### Coin-Klasse

```python
class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y)
    def collect()    # Entfernt den Coin aus dem Spiel
```

### Funktionsweise

1. **Beim Level-Laden**: 
   - Die World-Klasse sucht nach Tile-Wert 4 und 5
   - Für jedes gefundene Element wird ein Coin-Objekt erstellt
   - Coins werden in der `coin_group` gespeichert

2. **Während des Spiels**:
   - Coins werden mit Camera-Offset gezeichnet
   - Kollisionen werden mit dem Spieler erkannt
   - Gesammelte Coins werden entfernt

3. **Spieler-Tracking**:
   - `player.total_coins`: Gesamtanzahl der Coins im Level
   - `player.coins_collected`: Anzahl der eingesammelten Coins
   - Der Zähler wird oben links angezeigt

## Tipps

- **Strategie platzieren**: Coins sollten strategisch im Level verteilt sein
- **Mit Plattformen verbinden**: Platziere Coins auf Gras-Plattformen (Tile 2)
- **Challenge-Elemente**: Kombiniere Coins mit Feinden (Tile 3) oder Lava (Tile 6)
- **Visuelle Hilfsmittel**: Coins sind groß und auffällig - setze sie sichtbar!

## Zukünftige Erweiterungen

Mögliche Verbesserungen:
- [ ] Punkte-System basierend auf gesammelten Coins
- [ ] Level-Abschluss wenn alle Coins gesammelt sind
- [ ] Verschiedene Coin-Typen mit unterschiedlichen Werten
- [ ] Animations-Effekte beim Coin-Sammeln
- [ ] Sound-Effekte beim Sammeln
