from uscope.app.argus.scripting import ArgusScriptingPlugin

class Plugin(ArgusScriptingPlugin):
    def relay_on(self):
        """
        S5000
            not on
        S6000
            on
        """
        self.motion().command("M3 S10000")

    def relay_off(self):
        self.motion().command("M5")

    def run_test(self):
        while True:
            self.relay_on()
            self.sleep(1)
            # continue
            self.relay_off()
            self.sleep(1)

    def cleanup(self):
        self.relay_off()
