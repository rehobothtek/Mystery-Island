"""Command-line entry point for Mystery Island."""

from game import apply_action, available_actions, new_game


TITLE = """
=== MYSTERY ISLAND: THE LOST LIGHTHOUSE ===
Restore the beacon before your energy runs out.
Moves cost one energy. Collect the rope and lantern, cross the bridge,
then light the beacon. Commands ignore extra spaces and capital letters.
"""


def play_game():
    """Run one complete interactive game and return when it has ended."""
    print(TITLE)
    name = input("What is your name, explorer? ").strip()
    player = new_game(name)
    print("Welcome, {}. You wake on the Beach with 5 energy.".format(player["name"]))

    while not player["game_over"]:
        print("\nLocation: {} | Energy: {}".format(player["location"], player["energy"]))
        print("Choices: {}".format("; ".join(available_actions(player))))
        result = apply_action(player, input("> "))
        print(result["message"])

    if player["won"]:
        print("Victory! You made it home safely.")
    elif player["energy"] == 0:
        print("Defeat. The island grows quiet as the rescue boat sails past.")


def main():
    """Offer replay after each completed game."""
    while True:
        play_game()
        replay = input("Play again? (y/n): ").strip().lower()
        if replay not in {"y", "yes"}:
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
