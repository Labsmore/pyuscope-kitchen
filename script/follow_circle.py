"""
WARNING: this script is very much a PoC
It uses advanced pyuscope APIs that are not recommended for general use / have some bugs
"""

from uscope.app.argus.scripting import ArgusScriptingPlugin
import time
import math
"""
Return end point given a starting point on a circle and how far you want it to travel
Inspired by
https://stackoverflow.com/questions/11462239/how-to-move-point-along-circle

Angle calculated from +X axis extending to right
Going CCW => negative angle
(CCW => follow watch)
"""


def move_circle_cw(center, radius, start, travel, log=None):
    # Calculate starting angle
    start_angle = math.atan(
        (start["y"] - center["y"]) / (start["x"] - center["x"]))
    if start["x"] < center["x"]:
        start_angle = -(3.14 - start_angle)

    # log(f"start angle {start_angle} {start_angle * 180 / 3.14}")
    # How far do we need to travel?
    fraction = travel / (2 * 3.14 * radius)
    # - => CCW
    end_angle = start_angle - fraction * 2 * 3.14
    # log(f"end angle {end_angle} {end_angle * 180 / 3.14}")
    ret_x = center["x"] + radius * math.cos(end_angle)
    ret_y = center["y"] + radius * math.sin(end_angle)
    return {"x": ret_x, "y": ret_y}


def test():
    # 2 * 3.14 * 10.0 = 62.8 circumference
    # quarter => 15.7
    # expect to end around {"x": 0.0, "y": -10.0}
    # {'x': 9.999996829318347, 'y': 0.007963267107334854}
    """
    {'x': 0.007963267107334854, 'y': -9.999996829318347}
    {'x': -9.999987317275394, 'y': -0.01592652916487272}
    {'x': -0.023889781122824267, 'y': 9.99997146387718}
    {'x': 9.999949269133753, 'y': 0.03185301793138878}
    """
    print(
        move_circle_cw({
            "x": 0.0,
            "y": 0.0
        },
                       10.0, {
                           "x": 10.0,
                           "y": 0.0
                       },
                       travel=15.7))
    print(
        move_circle_cw({
            "x": 0.0,
            "y": 0.0
        },
                       10.0, {
                           "x": 10.0,
                           "y": 0.0
                       },
                       travel=2 * 15.7))
    print(
        move_circle_cw({
            "x": 0.0,
            "y": 0.0
        },
                       10.0, {
                           "x": 10.0,
                           "y": 0.0
                       },
                       travel=3 * 15.7))
    print(
        move_circle_cw({
            "x": 0.0,
            "y": 0.0
        },
                       10.0, {
                           "x": 10.0,
                           "y": 0.0
                       },
                       travel=4 * 15.7))


class Plugin(ArgusScriptingPlugin):
    def run_test(self):
        # Circle radius
        # We start in center
        radius = 13
        # Control loop update frequency
        period = 0.2
        # magic...
        queue_fix = 0.70
        verbose = False

        motion = self.motion()
        last = time.time()
        origin = self.pos()
        velocities = motion.get_max_velocities()

        # Fraction of max velocity
        machine_max_velocity = velocities["x"] / 60.0
        # max_velocity = machine_max_velocity * 0.15
        # Travel the circumference once per minute
        max_velocity = 2 * 3.14 * radius / 60 * 1.5
        assert max_velocity < machine_max_velocity

        motion.jog_cancel()
        try:
            # Move to starting position on circle
            self.move_absolute({"x": origin["x"] + radius})
            # Control loop
            self.log(f"origin {origin}")
            self.log(f"velocities {velocities}")
            while True:
                verbose and self.log("")
                pos = self.pos()
                verbose and self.log(f"pos {pos}")
                off_center = {
                    "x": pos["x"] - origin["x"],
                    "y": pos["y"] - origin["y"]
                }
                verbose and self.log(f"off center {off_center}")

                # How far we'll travel in the period
                # Assume x and y same speed
                travel = max_velocity * period * queue_fix
                verbose and self.log(f"travel {travel} of {2 * 3.14 * radius}")
                end_pos = move_circle_cw(origin,
                                         radius,
                                         pos,
                                         travel,
                                         log=self.log)
                deltas = {
                    "x": end_pos["x"] - pos["x"],
                    "y": end_pos["y"] - pos["y"]
                }

                rate = max(1, max_velocity * 60)
                # rate = 100
                verbose and self.log(f"jog_rel {deltas} @ {rate}")
                motion.jog_rel(deltas, rate=rate)

                # Sync to expected rate
                dt = time.time() - last
                sleeping = max(0, period - dt)
                verbose and self.log(f"sleep {sleeping}")
                self.sleep(sleeping)
                last = time.time()
        # 2023-10-31
        # Something is wrong with cleanup
        # Stuck in jog state at end...
        finally:
            self.log("cleaning up")
            # wait for jog to finish
            self.sleep(period * 2)
            self.sleep(1)
            motion.jog_cancel()
            self.sleep(1)
            self.move_absolute(origin)


if __name__ == "__main__":
    test()
