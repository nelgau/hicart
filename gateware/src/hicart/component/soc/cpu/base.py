from abc import ABCMeta, abstractproperty

from amaranth_soc.periph import ConstantInt


__all__ = ["CPU", "ConstantAddr"]


class CPU(metaclass=ABCMeta):
    """TODO
    """
    name       = abstractproperty()
    arch       = abstractproperty()
    byteorder  = abstractproperty()
    data_width = abstractproperty()
    reset_addr = abstractproperty()
    muldiv     = abstractproperty()


class ConstantAddr(ConstantInt):
    def __init__(self, value, *, width=None):
        return super().__init__(value, width=width, signed=False)

    def __repr__(self):
        return "ConstantAddr({}, width={})".format(self.value, self.width)
