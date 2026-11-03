"""Acceptance tests for Mystery Island game rules."""

import copy
import unittest

from game import apply_action, is_win, new_game


class MysteryIslandTests(unittest.TestCase):
    def move_to(self, player, *actions):
        for action in actions:
            apply_action(player, action)

    def test_new_game_has_required_starting_state(self):
        player = new_game("Ada")
        self.assertEqual("Beach", player["location"])
        self.assertEqual(5, player["energy"])
        self.assertEqual([], player["inventory"])

    def test_invalid_command_does_not_change_state(self):
        player = new_game()
        before = copy.deepcopy(player)
        result = apply_action(player, "banana")
        self.assertFalse(result["changed"])
        self.assertEqual(before, player)

    def test_legal_move_changes_location_and_costs_one_energy(self):
        player = new_game()
        apply_action(player, "go jungle")
        self.assertEqual("Jungle", player["location"])
        self.assertEqual(4, player["energy"])

    def test_wrong_direction_is_rejected_without_cost(self):
        player = new_game()
        apply_action(player, "go cave")
        self.assertEqual("Beach", player["location"])
        self.assertEqual(5, player["energy"])

    def test_rope_can_be_collected_only_once(self):
        player = new_game()
        apply_action(player, "take rope")
        result = apply_action(player, "take rope")
        self.assertEqual(["rope"], player["inventory"])
        self.assertFalse(result["changed"])

    def test_bridge_cannot_be_crossed_without_rope(self):
        player = new_game()
        self.move_to(player, "go jungle", "go cave", "go bridge")
        energy_before = player["energy"]
        apply_action(player, "go lighthouse")
        self.assertEqual("Old Bridge", player["location"])
        self.assertEqual(energy_before, player["energy"])

    def test_lighthouse_cannot_be_lit_without_lantern(self):
        player = new_game()
        self.move_to(player, "take rope", "go jungle", "go cave", "go bridge", "go lighthouse")
        self.assertEqual("Lighthouse", player["location"])
        apply_action(player, "light beacon")
        self.assertFalse(is_win(player))
        self.assertFalse(player["game_over"])

    def test_correct_inventory_at_lighthouse_wins(self):
        player = new_game()
        self.move_to(player, "take rope", "go jungle", "take lantern", "go cave", "go bridge", "go lighthouse")
        apply_action(player, "light beacon")
        self.assertTrue(is_win(player))
        self.assertTrue(player["game_over"])

    def test_energy_exhaustion_ends_game_without_negative_energy(self):
        player = new_game()
        self.move_to(player, "go jungle", "go beach", "go jungle", "go beach", "go jungle")
        self.assertEqual(0, player["energy"])
        self.assertTrue(player["game_over"])

    def test_replay_state_is_fresh(self):
        old_player = new_game()
        apply_action(old_player, "take rope")
        apply_action(old_player, "go jungle")
        fresh_player = new_game()
        self.assertEqual("Beach", fresh_player["location"])
        self.assertEqual(5, fresh_player["energy"])
        self.assertEqual([], fresh_player["inventory"])

    def test_input_is_trimmed_and_case_insensitive(self):
        player = new_game()
        apply_action(player, "  TAKE ROPE  ")
        self.assertIn("rope", player["inventory"])


if __name__ == "__main__":
    unittest.main()
