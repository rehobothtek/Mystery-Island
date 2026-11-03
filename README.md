# Mystery Island: The Lost Lighthouse

A beginner-friendly Python text adventure. You wake on a stormy island and
must restore a lighthouse beacon before a rescue boat passes by.

## Requirements and setup

Use Python 3.10 or newer. No third-party packages are needed.

```powershell
python main.py
python -m unittest discover -s tests -v
```

## Rules and controls

- You start on the **Beach** with 5 energy and an empty inventory.
- Legal moves cost one energy. At zero energy, you lose; energy never goes
  below zero.
- Travel through all five locations: Beach, Jungle, Cave, Old Bridge, and
  Lighthouse.
- Collect the **rope** on the Beach and **lantern** in the Jungle. Each can
  be picked up only once.
- The rope is required to cross from Old Bridge to Lighthouse. The lantern is
  required to light the beacon.
- Type the displayed commands, `inventory`, `help`, or `quit`. Commands are
  case-insensitive and accept surrounding spaces.
- `climb tree` spends energy for a view; `rest` in the Cave restores one
  energy once (up to the starting maximum). These optional choices have clear
  consequences.

A successful route is: `take rope`, `go jungle`, `take lantern`, `go cave`,
`go bridge`, `go lighthouse`, `light beacon`.

## Design

`game.py` contains deterministic, testable game rules. `main.py` only handles
terminal input and output. The inventory is a list because the player carries
a changing collection of unique item names. `new_game()` creates a new list on
each replay, preventing old items from leaking into a new run.

## Known limits

This is a single-player terminal game with no saved progress, map display, or
random events. It uses simple text commands rather than numbered menus.
