"""Rules and state transitions for the Mystery Island text adventure.

This module deliberately contains no calls to input() or print(), making the
game rules straightforward to test independently from the command-line UI.
"""

STARTING_ENERGY = 5


def new_game(name="Explorer"):
    """Return a fresh player state for a new game."""
    return {
        "name": name.strip() or "Explorer",
        "location": "Beach",
        "energy": STARTING_ENERGY,
        "inventory": [],
        "game_over": False,
        "won": False,
        "cave_rested": False,
    }


def available_actions(player):
    """Return commands that are useful at the player's current location."""
    common = ["inventory", "help", "quit"]
    location_actions = {
        "Beach": ["go jungle", "take rope"],
        "Jungle": ["go beach", "go cave", "take lantern", "climb tree"],
        "Cave": ["go jungle", "go bridge", "rest"],
        "Old Bridge": ["go cave", "go lighthouse"],
        "Lighthouse": ["go bridge", "light beacon"],
    }
    return location_actions[player["location"]] + common


def is_win(player):
    """Return whether the player has restored the beacon and escaped."""
    return player["won"]


def _result(message, changed=False):
    return {"message": message, "changed": changed}


def _spend_energy(player):
    """Spend one energy for a legal move and end the game at zero energy."""
    player["energy"] = max(0, player["energy"] - 1)
    if player["energy"] == 0:
        player["game_over"] = True
        return " Your energy is gone before rescue can find you."
    return ""


def _move(player, destination):
    """Move to destination, applying bridge and energy rules."""
    if player["location"] == "Old Bridge" and destination == "Lighthouse":
        if "rope" not in player["inventory"]:
            return _result("The broken bridge needs a rope. You cannot cross yet.")

    player["location"] = destination
    ending = _spend_energy(player)
    return _result("You travel to {}.{}".format(destination, ending), changed=True)


def apply_action(player, action):
    """Apply one normalized command to *player* and return a result dictionary.

    Invalid commands and blocked attempts never mutate the player state or
    consume energy.  A result has a human-readable ``message`` and ``changed``
    flag for the user interface.
    """
    if player["game_over"]:
        return _result("This game has already ended. Start a replay to continue.")

    command = action.strip().lower()
    if command == "quit":
        player["game_over"] = True
        return _result("You leave Mystery Island. Thanks for playing!", changed=True)
    if command == "inventory":
        items = ", ".join(player["inventory"]) or "nothing"
        return _result("Inventory: {}. Energy: {}.".format(items, player["energy"]))
    if command == "help":
        return _result("Try one of: {}.".format(", ".join(available_actions(player))))

    location = player["location"]
    routes = {
        "Beach": {"go jungle": "Jungle"},
        "Jungle": {"go beach": "Beach", "go cave": "Cave"},
        "Cave": {"go jungle": "Jungle", "go bridge": "Old Bridge"},
        "Old Bridge": {"go cave": "Cave", "go lighthouse": "Lighthouse"},
        "Lighthouse": {"go bridge": "Old Bridge"},
    }
    if command in routes[location]:
        return _move(player, routes[location][command])

    pickups = {"Beach": ("take rope", "rope"), "Jungle": ("take lantern", "lantern")}
    if location in pickups and command == pickups[location][0]:
        item = pickups[location][1]
        if item in player["inventory"]:
            return _result("You already picked up the {}.".format(item))
        player["inventory"].append(item)
        return _result("You pick up the {}.".format(item), changed=True)

    if location == "Jungle" and command == "climb tree":
        ending = _spend_energy(player)
        return _result("You climb for a better view, but it costs energy.{}".format(ending), changed=True)
    if location == "Cave" and command == "rest":
        if player["cave_rested"]:
            return _result("The cave is too cold to rest here again.")
        player["cave_rested"] = True
        player["energy"] = min(STARTING_ENERGY, player["energy"] + 1)
        return _result("You rest by a warm spring and recover one energy.", changed=True)
    if location == "Lighthouse" and command == "light beacon":
        if "lantern" not in player["inventory"]:
            return _result("The beacon is dark. You need the lantern to light it.")
        player["won"] = True
        player["game_over"] = True
        return _result("The beacon shines! A rescue boat sees it. You escape Mystery Island!", changed=True)

    return _result("That is not a valid action here. Type 'help' to see your choices.")
