import unittest
import model.units.api as uapi
from model.board_state import BoardState
from model.resources import ResType


class TestUnits(unittest.TestCase):
    def setUp(self) -> None:
        self.board = BoardState(['Aaron', 'Sandra', 'Ezra', 'Dave', 'Jeff'])
        self.aaron = self.board.players[0]
        self.sandra = self.board.players[1]

    def test_cost_str(self):
        self.assertEqual(uapi.Constructor.cost_str(), "1B, 1C, 1Si, 1U")
        self.assertEqual(uapi.Zergling.cost_str(), "1B, 3C")
        self.assertEqual(uapi.Hydralisk.cost_str(), "2B, 5C, Sac:Zergling")
        self.assertEqual(uapi.Nuke.cost_str(), "4Si, Sac:3xEnrichedUranium")

    def test_stem_cell(self):
        self.board.add_unit(uapi.StemCell, self.aaron)
        my_stem_cell = self.board.units[self.aaron][2]
        self.assertEqual(self.aaron.resources[ResType.BUILDS], 2)
        self.assertEqual(len(self.board.units[self.aaron]), 3)
        my_stem_cell.activate(None)
        self.assertEqual(self.aaron.resources[ResType.BUILDS], 4)
        self.assertEqual(len(self.board.units[self.aaron]), 2)

    def test_inits(self):
        class_names = (name for name in dir(uapi) if not name.startswith("_"))
        # Build some units to sacrifice
        # For Hydralisk
        self.board.add_unit(uapi.Zergling, self.aaron)
        # For Queen
        self.board.add_unit(uapi.Zergling, self.aaron)
        # For Ultralisk
        self.board.add_unit(uapi.Zergling, self.aaron)
        self.board.add_unit(uapi.Hydralisk, self.aaron)
        # For Nuke
        self.board.add_unit(uapi.EnrichedUranium, self.aaron)
        self.board.add_unit(uapi.EnrichedUranium, self.aaron)
        self.board.add_unit(uapi.EnrichedUranium, self.aaron)
        self.board.add_unit(uapi.EnrichedUranium, self.aaron)
        self.board.add_unit(uapi.EnrichedUranium, self.aaron)
        for unit_type in ((getattr(uapi, c_name) for c_name in class_names)):
            self.board.add_unit(unit_type, self.aaron)


if __name__ == '__main__':
    unittest.main()

