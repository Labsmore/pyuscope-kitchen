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
from uscopek.illuminator.relay_illuminator import QuadRelayIlluminator
import os


class Plugin(ArgusScriptingPlugin):
    def input_config(self):
        return {
            "row1": {
                "widget": "QPushButtons",
                "buttons": {
                    "NW": "nw",
                    "N": "n",
                    "NE": "ne",
                },
            },
            "row2": {
                "widget": "QPushButtons",
                "buttons": {
                    "W": "w",
                    "All": "all",
                    "E": "e",
                },
            },
            "row3": {
                "widget": "QPushButtons",
                "buttons": {
                    "SW": "sw",
                    "S": "s",
                    "SE": "se",
                },
            },
            "row4": {
                "widget": "QPushButtons",
                "buttons": {
                    "Cycle": "cycle",
                },
            },
        }

    def show_run_button(self):
        return False

    def run_test(self):
        quad = QuadRelayIlluminator()

        vals = self.get_input()
        button = vals.get("button")
        if button:
            if button["value"] == "cycle":
                while True:
                    for mode in ("all", "n", "ne", "e", "se", "s", "sw", "w",
                                 "nw"):
                        quad.mode(mode)
                        self.sleep(0.5)
            else:
                quad.mode(button["value"])

        if 0:
            self.log("Cycling relays")

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
