# epaperboard
epaperboard is a Python application to build a dashboard using a Raspberry Pi and an e-paper (aka e-ink) display!

image

Why e-paper? Two main reasons:

* It doesn't emmit light, so I can have this in my living room without being disturbing at night;
* I love the grayscale aesthetics these displays provide!

# Requirements

## Hardware

This application should work with any Raspberry Pi board with a GPIO header and any Waveshare e-paper display 
with a parallel interface using the IT8951 HAT. Mind that not all Waveshare e-paper displays use that driver.
If you have a SPI display that connects to the Raspberry Pi through the SPI pins or the simpler passive HAT,
you need to write a display adapter.

Here's what I'm using:

* [Raspberry Pi 3](https://www.raspberrypi.org/products/raspberry-pi-3-model-b/?resellerType=home)
* [Waveshare 800x600, 6inch E-Ink display HAT](https://www.waveshare.com/product/raspberry-pi/displays/e-paper/6inch-e-paper-hat.htm)
* (optional) [8x10 Shadow Box with Slot](https://www.amazon.ca/gp/product/B07YCHSDLN/)

Any Raspberry Pi model with a GPIO header should work. Any e-paper display with a IT8951 should also work, but
you will need to adjust the drawing code to the resolution of the display you're using. This specific model gives
you 16 levels of grayscale.

The easiest way to wire the display to the Raspberry Pi is to plug the HAT directly to the GPIO headers, but
you may also use the SPI cable provided with the display to connect it directly to the SPI pins. This may be
useful if you're using a Pi Zero W, which does not come with the header pins soldered.

I also got a shadow box to use as an enclosure. If you choose (or print) an enclosure for your dashboard,
keep in mind the Pi with the HAT is bulky, especially due to the headers the HAT comes with for programming
the driver chip. The one linked above is just deep enough to fit everything inside. I used tape to stick the
display to the front glass and some spacers to screw the raspberry pi to the back. Finally, a blue poster board
is covering the glass to block the light from the LEDs inside (the HAT has a "power" LED, and the Pi has another one).

As a side note, the screen is not totally opaque, and at night I can still see a faint red glow from the LED behind
the screen. If you want to block all light coming from the electronics, you need to cover the back of the screen with
some material to block the light.

## Software

You'll need:

* Python 3.7 or newer, which comes pre-installed with the Raspberry Pi OS. I'm using 3.7.3 without issues.
* [Greg Meyer's IT8951 Python library](https://github.com/GregDMeyer/IT8951). This awesome Python library talks to
the driver HAT through its serial protocol and provides a very simple API to work with the Waveshare display. Follow
the instructions on the project page to install it.
* pip3 to install both Greg's library and the application.

# Installation

1. Install the following packages. The first one is a library needed by `pillow` that's missing and would cause
a runtime error if not installed. The second one is the Pypi package manager.

```
sudo apt-get install libopenjp2-7
sudo apt-get install python3-pip
```

2. Follow the instructions on [Greg's IT8951 library page'](https://github.com/GregDMeyer/IT8951) to install it.
Note you need to use `pip3` instead of `pip`. As the page mentions, make sure you enable SPI with `raspi-config`.

3. Checkout this repository to a directory somewhere in your Raspberry pi, `cd` into it and run `pip3 install .`:

```
git clone https://github.com/arroz/epaperboard
cd epaperboard
pip3 install .
```

The application is now installed in your home directory.

