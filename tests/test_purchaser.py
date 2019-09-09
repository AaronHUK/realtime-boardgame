import unittest

from model import purchaser, board_state
from model.resources import ResType
from model.units.api import TarPit, StemCell, Zergling, Hydralisk
from model.exceptions import RequestException


class TestPurchaser(unittest.TestCase):
    def setUp(self) -> None:
        self.board = board_state.BoardState(['Aaron', 'Sandra', 'Ezra', 'Dave', 'Jeff'])
        self.aaron = self.board.players[0]
        self.sandra = self.board.players[1]
        self.purchaser = purchaser.Purchaser(self.board)

    def test_request(self):
        with self.assertRaises(RequestException):
            self.purchaser.request(self.aaron, StemCell)
        # The purchase should have failed
        self.assertEqual(len(self.board.units[self.aaron]), 2)
        self.purchaser.request(self.aaron, TarPit)
        # The purchase should have succeeded
        self.assertEqual(len(self.board.units[self.aaron]), 3)
        with self.assertRaises(RequestException):
            self.purchaser.request(self.aaron, TarPit)
        self.assertEqual(len(self.board.units[self.aaron]), 3)
        self.sandra.add_resource(ResType.CARBON, 10)
        with self.assertRaises(RequestException):
            self.purchaser.request(self.sandra, Hydralisk)


if __name__ == '__main__':
    unittest.main()
