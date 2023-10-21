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


def pin_signature(width, dir):
    members = {}
    if dir in ("i", "io"):
        members["i"] = In(width)
    if dir in ("o", "oe", "io"):
        members["o"] = Out(width)
    if dir in ("oe", "io"):
        members["oe"] = Out(1)
    return wiring.Signature(members)
