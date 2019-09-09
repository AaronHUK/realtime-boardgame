from model.units import api


def unit_sort(name):
    return getattr(api, name).sort
