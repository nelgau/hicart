class QSPIFlashEmulator:
    def __init__(self, bus):
        self.bus = bus

    def begin(self):
        self.bus.d.i.setimmediatevalue(0)
