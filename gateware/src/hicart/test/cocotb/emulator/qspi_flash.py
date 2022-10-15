class QSPIFlashEmulator:
    def __init__(self, bus):
        self.bus = bus

    async def begin(self):
        self.bus.d.i.setimmediatevalue(0)
