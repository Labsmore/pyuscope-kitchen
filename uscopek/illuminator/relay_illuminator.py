from uscopek.relay import sain_smart


class QuadRelayIlluminator:
    def __init__(self, ssrelay=None):
        if ssrelay is None:
            ssrelay = sain_smart.SSRelay8CH()
        self.ssrelay = ssrelay
        """
        Power cord to upper right
        Common red (+V/+I)
        """
        # Make this configurable?
        self.quad2ch = {
            "ne": 0,
            "se": 1,
            "sw": 2,
            "nw": 3,
        }

    def __del__(self):
        self.close()

    def close(self):
        self.ssrelay.close()

    def all_on(self):
        self.ssrelay.all_on()

    def all_off(self):
        self.ssrelay.all_off()

    def nw(self):
        self.ssrelay.relay_on(self.quad2ch["nw"])

    def ne(self):
        self.ssrelay.relay_on(self.quad2ch["ne"])

    def se(self):
        self.ssrelay.relay_on(self.quad2ch["se"])

    def sw(self):
        self.ssrelay.relay_on(self.quad2ch["sw"])

    def corners(self):
        return self.quad2ch.keys()

    def mode(self, mode):
        if mode == "none":
            self.all_off()
        elif mode == "all":
            self.all_on()
        elif mode == "n":
            self.ssrelay.relays_on((self.quad2ch["nw"], self.quad2ch["ne"]))
        elif mode == "e":
            self.ssrelay.relays_on((self.quad2ch["ne"], self.quad2ch["se"]))
        elif mode == "s":
            self.ssrelay.relays_on((self.quad2ch["sw"], self.quad2ch["se"]))
        elif mode == "w":
            self.ssrelay.relays_on((self.quad2ch["nw"], self.quad2ch["sw"]))
        elif mode in self.quad2ch:
            self.ssrelay.relay_on(self.quad2ch[mode])
        else:
            assert 0, f"bad mode {mode}"
