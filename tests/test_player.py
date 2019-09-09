import unittest

from model import player
from model import magics
from model.resources import ResType
from model.exceptions import ModelException


class TestPlayer(unittest.TestCase):
    def setUp(self) -> None:
        self.player = player.Player('Aaron')

    def test_add_resources(self):
        for res in ResType:
            self.assertEqual(self.player.resources[res], magics.INIT[res],
                             "On <{}> magics <{}> actual <{}>".format(
                             res, magics.INIT[res], self.player.resources[res]))

        self.player.add_resource(ResType.BUILDS, 2)
        self.assertEqual(self.player.resources[ResType.BUILDS], magics.INIT[ResType.BUILDS] + 2)
        for res in ResType:
            self.player.add_resource(res, 2 * magics.MAX[res])
            self.assertEqual(self.player.resources[res], magics.MAX[res],
                             "On <{}> magics <{}> actual <{}>".format(
                             res, magics.MAX[res], self.player.resources[res]))

    def test_remove_resources(self):
        self.player.remove_resource(ResType.BUILDS, 1)
        self.assertEqual(self.player.resources[ResType.BUILDS], 1)
        with self.assertRaises(ModelException):
            self.player.remove_resource(ResType.BUILDS, 2)


if __name__ == '__main__':
    unittest.main()
