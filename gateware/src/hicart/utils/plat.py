import itertools

from amaranth import *
from amaranth.build import *
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out


def get_all_resources(platform, name):
    resources = []
    for number in itertools.count():
        try:
            resources.append(platform.request(name, number))
        except ResourceError:
            break
    return resources


class TristateSignature(wiring.Signature):
    def __init__(self, width):
        super().__init__({
            "i": In(width),
            "o": Out(width),
            "oe": Out(1),
        })
