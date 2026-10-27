# Escape the Ship

A turn-based simulation in Python where a bot must reach an escape button on a ship while fire spreads each turn. The player chooses from four bots, each using a different strategy:

- **Bot 1:** plans its route once at the start and never re-checks the fire
- **Bot 2:** replans every turn, but waits if the fire blocks every path
- **Bot 3:** takes the safest route away from the fire, even if it's the longest
- **Bot 4:** predicts where the fire will spread and plans around it

The project compares how each strategy fails, and what that shows about balancing safety, speed and adaptability.
