"""
SRD-12VDC-SL-C
SainSmart USB Eight Channel Relay Board for Automation - 12 V
https://www.amazon.com/gp/product/B0093Y89DE/

http://wiki.sainsmart.com/index.php/101-70-116

maybe we should use a library instead?
saw this but its GPL
https://github.com/darrylb123/usbrelay
"""

from uscope.app.argus.scripting import ArgusScriptingPlugin
from pylibftdi import BitBangDevice
import os


class SSRelay8CH:
    def __init__(self):
        self.bb = BitBangDevice(
            port=
            "/dev/serial/by-id/usb-FTDI_FT245R_USB_FIFO_AB0NXIZM-if00-port0")
        # All output
        self.bb.direction = 0xFF

    def __del__(self):
        self.close()

    def close(self):
        self.bb.close()

    def on(self, relay):
        assert 0 <= relay <= 7
        self.bb.port |= 1 << relay

    def all_off(self):
        self.bb.port = 0

    def all_on(self):
        self.bb.port = 0xFF

    def relay_on(self, relay):
        assert 0 <= relay <= 7
        self.bb.port = 1 << relay

    def relays_on(self, relays):
        #assert 0 <= relay <= 7
        self.bb.port = sum([1 << relay for relay in relays])

    def relay_off(self, relay):
        assert 0 <= relay <= 7
        self.bb.port &= 0xFF ^ (1 << relay)

    def relay_toggle(self, relay):
        assert 0 <= relay <= 7
        self.bb.port ^= 1 << relay


class QuadIlluminator:
    def __init__(self, ssrelay=None):
        if ssrelay is None:
            ssrelay = SSRelay8CH()
        self.ssrelay = ssrelay
        """
        Power cord to upper right
        Common red (+V/+I)
        """
        self.quad2ch = {
            "ul": 1,
            "ur": 0,
            "lr": 2,
            "ll": 3,
        }

    def __del__(self):
        self.close()

    def close(self):
        self.ssrelay.close()

    def all_on(self):
        self.ssrelay.all_on()

    def all_off(self):
        self.ssrelay.all_off()

    def ul(self):
        self.ssrelay.relay_on(self.quad2ch["ul"])

    def ur(self):
        self.ssrelay.relay_on(self.quad2ch["ur"])

    def lr(self):
        self.ssrelay.relay_on(self.quad2ch["lr"])

    def ll(self):
        self.ssrelay.relay_on(self.quad2ch["ll"])

    def corners(self):
        return self.quad2ch.keys()

    # XXX: maybe switch to compass directions
    def mode(self, mode):
        if mode == "none":
            self.all_off()
        elif mode == "all":
            self.all_on()
        elif mode == "up":
            self.ssrelay.relays_on((self.quad2ch["ul"], self.quad2ch["ur"]))
        elif mode == "right":
            self.ssrelay.relays_on((self.quad2ch["ur"], self.quad2ch["lr"]))
        elif mode == "down":
            self.ssrelay.relays_on((self.quad2ch["ll"], self.quad2ch["lr"]))
        elif mode == "left":
            self.ssrelay.relays_on((self.quad2ch["ul"], self.quad2ch["ll"]))
        elif mode in self.quad2ch:
            self.ssrelay.relay_on(self.quad2ch[mode])
        else:
            assert 0, f"bad mode {mode}"


class Plugin(ArgusScriptingPlugin):
    def run_test(self):
        self.log("Cycling relays")

        quad = QuadIlluminator()
        quad.lr()
        dir_out = "relay_demo"
        if not os.path.exists(dir_out):
            os.mkdir(dir_out)

        try:
            quad.mode("all")
            self.sleep(1)
            for mode in ("all", "up", "right", "down", "left", "ul", "ur",
                         "lr", "ll"):
                self.log(f"On: {mode}")
                quad.mode(mode)
                # Give auto-exposure some time
                self.sleep(0.4)
                im = self.image()
                im.save(os.path.join(dir_out, f"{mode}.jpg"), quality=90)
            quad.mode("ll")
        finally:
            quad.close()
