from collections import OrderedDict
from amaranth.hdl.rec import Layout


class Accessor:
    @staticmethod
    def get(layout):
        def construct(dut, name=None):
            return Accessor(dut, layout, name=name)
        return construct

    def __init__(self, dut, layout, name=None):
        self.dut = dut
        self.name = name

        self.layout = Layout.cast(layout)
        self.fields = OrderedDict()

        def concat(a, b):
            if a is None:
                return b
            return "{}__{}".format(a, b)

        for field_name, field_shape, _ in self.layout:
            full_name = concat(name, field_name)
            if isinstance(field_shape, Layout):
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
