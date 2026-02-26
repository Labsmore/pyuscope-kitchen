# Example PiCam2 + GRBL configuration with optics calculations explained

This is a snapshot of the configuration I use on my homebrew CNC microscope. At the time of writing it has:

  * Raspberry Pi 4 Model B + Raspberry Pi HQ Camera with a Pi Hut mounting plate
  * MKS GEN 1.4 controller (RAMPS 1.4 compatible, Atmega2560) with Trinamic motor drivers, running GRBL
  * Olympus BH2 / BHM metallurgical microscope

The goal of this is to give an example of what a typical microscope setup looks like using common hardware, and explain how some of the optical values are derived from microscope specifications.

With a bit of bookwork, it should be possible to take this configuration and use it to configure Pyuscope for a similar DIY microscope with a GRBL based motion controller. You'll need to know some basic specifications for your microscope, like the magnification factors of the components in the trinocular image path.

For more details, read the comments.

This configuration assumes GRBL on the motor driver is already configured. This means homing direction, steps per millimetre and maximum travel rates.

