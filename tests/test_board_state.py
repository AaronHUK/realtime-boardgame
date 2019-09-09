import unittest
from model import board_state
from model.resources import ResType
from model import magics
from model.units.api import *
from model.units.factories import res_growth
from model.exceptions import RequestException, ModelException
from collections import defaultdict


class TestBoardState(unittest.TestCase):
    def setUp(self) -> None:
        self.board = board_state.BoardState(player_names=["Aaron", "Sandra", "Ezra", "Dave", "Jeff"])
        self.aaron = self.board.players[0]
        self.sandra = self.board.players[1]
        self.ezra = self.board.players[2]
        self.dave = self.board.players[3]
        self.jeff = self.board.players[4]

    def tearDown(self) -> None:
        self.board.clear_all()

    def test_init_board(self):
        #new_board = board_state.BoardState(state=self.board.state)
        pass

    def test_add_unit(self):
        self.board.add_unit(TarPit, self.aaron)
        self.board.add_unit(Mine, self.ezra)
        self.board.add_unit(Mine, self.ezra)
        self.board.add_unit(Centrifuge, self.ezra)
        self.assertEqual(len(self.board.units[self.aaron]), 3)
        self.assertEqual(len(self.board.units[self.sandra]), 2)
        self.assertEqual(len(self.board.units[self.ezra]), 5)

    def test_add_unit_sacrifices(self):
        with self.assertRaises(ModelException):
            self.board.add_unit(Hydralisk, self.aaron)
        self.board.add_unit(Zergling, self.aaron)
        self.assertEqual(len(self.board.units[self.aaron]), 3)
        self.board.add_unit(Hydralisk, self.aaron)

    def test_attack(self):
        self.assertEqual(self.board.total_attack(self.aaron), 0)
        self.board.add_unit(Zergling, self.aaron)
        self.assertEqual(self.board.total_attack(self.aaron), 3)
        self.board.add_unit(Hydralisk, self.aaron)
        self.assertEqual(self.board.total_attack(self.aaron), 9)
        self.board.add_unit(FusionCannon, self.aaron)
        self.assertEqual(self.board.total_attack(self.aaron), 12)

    def test_defence(self):
        self.assertEqual(self.board.total_defence(self.aaron), 2)
        self.board.add_unit(FortifiedConstructor, self.aaron)
        self.assertEqual(self.board.total_defence(self.aaron), 9)
        self.board.add_unit(Deflector, self.aaron)
        self.assertEqual(self.board.total_defence(self.aaron), 12)
        self.board.add_unit(FusionCannon, self.aaron)
        self.assertEqual(self.board.total_defence(self.aaron), 14)

    def test_next_round(self):
        self.board.add_unit(TarPit, self.aaron)

        self.board.add_unit(Mine, self.aaron)
        self.board.add_unit(Mine, self.sandra)
        self.board.add_unit(Mine, self.sandra)
        self.board.add_unit(Mine, self.ezra)

        self.board.add_unit(Centrifuge, self.ezra)
        dave_fuges = [self.board.add_unit(Centrifuge, self.dave),
                      self.board.add_unit(Centrifuge, self.dave)]

        old_res = {res: [] for res in ResType}
        for res in ResType:
            old_res[res] = [player.resources[res] for player in self.board.players]
        self.board.next_round({})
        new_res = {res: [] for res in ResType}
        for res in ResType:
            new_res[res] = [player.resources[res] for player in self.board.players]
        # Carbon
        carbon_1_player = magics.GROWTH[ResType.CARBON][0]
        self.assertEqual(new_res[ResType.CARBON][0], old_res[ResType.CARBON][0] + carbon_1_player)
        self.assertEqual(new_res[ResType.CARBON][1], old_res[ResType.CARBON][1])

        silicon_3_player = magics.GROWTH[ResType.SILICON][2]
        self.assertEqual(new_res[ResType.SILICON][0], old_res[ResType.SILICON][0] + silicon_3_player)
        self.assertEqual(new_res[ResType.SILICON][1], old_res[ResType.SILICON][1] + (2 * silicon_3_player))
        self.assertEqual(new_res[ResType.SILICON][2], old_res[ResType.SILICON][2] + silicon_3_player)
        self.assertEqual(new_res[ResType.SILICON][3], old_res[ResType.SILICON][3])

        uranium_2_player = magics.GROWTH[ResType.URANIUM][1]
        self.assertEqual(new_res[ResType.URANIUM][0], old_res[ResType.URANIUM][0])
        self.assertEqual(new_res[ResType.URANIUM][2], old_res[ResType.URANIUM][2] + uranium_2_player)
        self.assertEqual(new_res[ResType.URANIUM][3], old_res[ResType.URANIUM][3] + (2 * uranium_2_player))

        for fuge in dave_fuges:
            fuge.on_death()

        self.board.next_round({})
        uranium_1_player = magics.GROWTH[ResType.URANIUM][0]
        self.assertEqual(self.ezra.resources[ResType.URANIUM], new_res[ResType.URANIUM][2] + uranium_1_player)

    def test_kill(self):
        self.board.kill(self.aaron, Constructor)
        self.assertEqual(len(self.board.units[self.aaron]), 1)
        self.board.kill(self.aaron, Constructor)
        self.assertEqual(len(self.board.units[self.aaron]), 0)
        with self.assertRaises(RequestException):
            self.board.kill(self.aaron, Constructor)

    def test_get_unit(self):
        self.board.add_unit(StemCell, self.aaron)
        self.board.add_unit(Zergling, self.sandra)
        self.board.get_unit(StemCell, self.aaron)
        with self.assertRaises(RequestException):
            self.board.get_unit(Zergling, self.aaron)
        self.board.get_unit(Zergling, self.sandra)
        self.board.get_unit(Constructor, self.sandra)

    def test_transfer_resources(self):
        expected_aaron = defaultdict(int)
        expected_sandra = defaultdict(int, {ResType.BUILDS: 4})
        self.board.transfer_resources(self.aaron, self.sandra)
        for res in ResType:
            self.assertEqual(self.aaron.resources[res], expected_aaron[res])
            self.assertEqual(self.sandra.resources[res], expected_sandra[res])
        self.aaron.add_resource(ResType.CARBON, 3)
        self.aaron.add_resource(ResType.SILICON, magics.MAX[ResType.SILICON] - 2)
        self.sandra.add_resource(ResType.SILICON, magics.MAX[ResType.SILICON] - 1)
        self.sandra.add_resource(ResType.URANIUM, 1)
        expected_sandra.update({ResType.CARBON: 3,
                                ResType.SILICON: magics.MAX[ResType.SILICON],
                                ResType.URANIUM: 1})
        self.board.transfer_resources(self.aaron, self.sandra)
        for res in ResType:
            self.assertEqual(self.aaron.resources[res], expected_aaron[res])
            self.assertEqual(self.sandra.resources[res], expected_sandra[res])
        self.board.transfer_resources(self.aaron, self.sandra)
        for res in ResType:
            self.assertEqual(self.aaron.resources[res], expected_aaron[res])
            self.assertEqual(self.sandra.resources[res], expected_sandra[res])
        self.board.transfer_resources(self.sandra, self.aaron)
        for res in ResType:
            self.assertEqual(self.aaron.resources[res], expected_sandra[res])
            self.assertEqual(self.sandra.resources[res], expected_aaron[res])

    def test_attack_player(self):
        self.aaron.attacking = True
        self.board.next_round({})
        self.board.next_round({self.aaron: self.sandra})
        self.assertIn(self.sandra, self.board.players)
        self.assertIn(self.sandra, self.board.units)
        self.board.add_unit(Zergling, self.sandra)
        self.aaron.attacking = True
        self.board.next_round({})
        self.board.next_round({self.aaron: self.sandra})
        self.assertFalse(self.aaron.attacking)
        self.assertIn(self.aaron, self.board.players)
        self.assertIn(self.sandra, self.board.players)
        self.board.add_unit(TarPit, self.aaron)
        self.board.add_unit(TarPit, self.sandra)
        self.assertEqual(res_growth(ResType.CARBON), magics.GROWTH[ResType.CARBON][1])
        self.sandra.attacking = True
        self.board.next_round({})
        self.aaron.remove_resource(ResType.BUILDS, magics.MAX[ResType.BUILDS] - 1)
        self.sandra.remove_resource(ResType.BUILDS, magics.MAX[ResType.BUILDS])
        self.assertEqual(self.sandra.resources[ResType.BUILDS], 0)
        self.assertEqual(self.aaron.resources[ResType.BUILDS], 1)
        self.board.next_round({self.sandra: self.aaron})
        self.assertFalse(self.sandra.attacking)
        self.assertIn(self.sandra, self.board.players)
        self.assertNotIn(self.aaron, self.board.players)
        self.assertNotIn(self.aaron, self.board.units)
        self.assertEqual(self.sandra.resources[ResType.BUILDS], 3)  # 2 growth + 1 from Aaron
        self.assertEqual(res_growth(ResType.CARBON), magics.GROWTH[ResType.CARBON][0])


if __name__ == '__main__':
    unittest.main()
