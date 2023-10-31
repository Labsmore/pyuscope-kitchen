"""
NOTE: the docs are really murky on the protocol
From what I can gather there are two versions of this device:
-One that uses a serial protocol using 3 byte packets
-Another that uses MPSSE bit banging (mine)

SainSmart USB Eight Channel Relay Board for Automation - 12 V
http://wiki.sainsmart.com/index.php/101-70-116
https://www.amazon.com/gp/product/B0093Y89DE/
Relay: SRD-12VDC-SL-C

maybe we should use a library instead?
https://github.com/darrylb123/usbrelay
    Maybe cool but GPL
    Could do CLI calls
"""

from pylibftdi import BitBangDevice


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
