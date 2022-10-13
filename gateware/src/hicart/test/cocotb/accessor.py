from collections import OrderedDict
from amaranth.hdl.rec import Layout


class Accessor:
    @staticmethod
    def from_layout(layout):
        root = _extract_tree(layout)
        return Accessor.from_tree(root)

    @staticmethod
    def from_names(names):
        root = [(n, None) for n in names]
        return Accessor.from_tree(root)

    @staticmethod
    def from_tree(root):
        def construct(dut, name=None):
            return Accessor(dut, root, name=name)
        return construct

    def __init__(self, dut, node, name=None):
        self.dut = dut
        self.node = node
        self.name = name

        self.fields = OrderedDict()

        def concat(a, b):
            if a is None:
                return b
            return "{}__{}".format(a, b)

        for field_name, field_shape in self.node:
            full_name = concat(name, field_name)
            if isinstance(field_shape, list):
                self.fields[field_name] = Accessor(dut, field_shape, name=full_name)
            else:
                self.fields[field_name] = getattr(dut, full_name)

    def __getattr__(self, name):
        return self[name]

    def __getitem__(self, item):
        try:
            return self.fields[item]
        except KeyError:
            if self.name is None:
                reference = "Unnamed accessor"
            else:
                reference = "Accessor '{}'".format(self.name)
            raise AttributeError("{} does not have a field '{}'. Did you mean one of: {}?"
                                    .format(reference, item, ", ".join(self.fields))) from None


def wishbone_accessor(dut, name=None, features=frozenset()):
    signal_names = _wishbone_signal_names(features)
    return Accessor.from_names(signal_names)(dut, name=name)


def _extract_tree(layout):
    layout = Layout.cast(layout)
    node = []
    for field_name, field_shape, _ in layout:
        if isinstance(field_shape, Layout):
            node += [(field_name, _extract_tree(field_shape))]
        else:
            node += [(field_name, None)]
    return node


def _wishbone_signal_names(features=frozenset()):
    names = ["adr", "dat_w", "dat_r", "sel", "cyc", "stb", "we", "ack"]
    features = set(features)
    if "err" in features:
        names += ["err"]
    if "rty" in features:
        names += ["rty"]
    if "stall" in features:
        names += ["stall"]
    if "lock" in features:
        names += ["lock"]
    if "cti" in features:
        names += ["cti"]
    if "bte" in features:
        names += ["bte"]
    return names
