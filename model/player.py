from . import magics
from model import resources
from model.exceptions import ModelException


class Player(object):
    def __init__(self, name):
        self.name = name
        self._resources = {res: magics.INIT[res] for res in resources.ResType}
        self.attacking = False

    def add_resource(self, resource, count):
        assert resource in resources.ResType
        self._resources[resource] = min(self._resources[resource] + count, magics.MAX[resource])

    def remove_resource(self, resource, count):
        if self._resources[resource] < count:
            raise ModelException("Unable to remove {} {}\nUnit resources {}".format(
                                 count, resource.name, self._resources))
        self._resources[resource] -= count
        assert self._resources[resource] >= 0

    @property
    def resources(self):
        return self._resources
