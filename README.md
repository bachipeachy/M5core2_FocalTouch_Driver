# FocalTouch_Driver_M5Stack_Core2
FocalTouch FT6X36 Driver in MicroPython for M5Stack Core2 hardware

## Introduction
This repository contains micropython driver (focaltouch.py) for FocalTouch FT6232 touch screen configured for M5Stack Core2 IOT device.
The code has been developed and tested on this hardware only.
The test script (focaltouch_test.py) excercises the main user methods supported by the driver.
The test script will run on stock Micropython firmware.

## Installation
The focaltouch.py driver may be installed in the M5Core2 flash memory under /lib folder without the need to compile the micropython source.
The driver can be renamed to avoid conflict if there is a duplicate driver with same name in the firmware.
As a more efficient alternative, the micropython source may be recompiled using esp32 IDF v4.4 with latest micropython source.

### Sample Test Environment with stock Micropython firmware
1. git clone https://github.com/bachipeachy/FocalTouch_Driver_M5Stack_Core2
2. Download stock vanilla micropython firmware v1.18 from the site https://micropython.org/download/esp32/
3. Flash the micropython firmware using Thonny IDE https://thonny.org
4. Create a new dir /lib in Thonny IDE and click on lib folder

#### Testing FocalTouch Driver -- Console Output Only
* Open files focaltouch.py and axp202c.py in Thonny and save them to M5Core2 flash /lib
* Open file focaltouch_test.py and run the script 
* There are four test choices -- run them one after another in any order


## Features
The driver supports following gestures:

TAP -- single touch tap with tunable timing threshold to delay sensing (touched_th=25 scans)

HOLD -- single touch hold with tunable hold time threshold exceeding (held_th=250 scans)

LEFT -- single touch left swipe

RIGHT -- single touch right swipe

UP -- single touch up swipe

DOWN -- single touch down swipe

NOTE: There are two tunable parameters for minimum swipe distances in pixels, atleast one of which must be exceeded to regster as a swipe. These are delta_x_th=32, delta_y_th=24 in x and y directions respectively. If atleast one thereshold is not reached, it will be registered as a "TAP" or "HOLD" depending on the speed of swipe.

## Usage

### method btn_gesture()

A single FocalTouch class method "btn_gesture()" supports all the above gestures as a possible return value.

from focaltouch import FocalTouch

ft = FocalTouch

btn = ft.btn_gesture(i2c, address=_FT6206_DEFAULT_I2C_ADDR, debug=False, btns=None, touched_th=25, held_th=250, delta_x_th=32, delta_y_th=24)

The parm "btns" must be a dictionary of btns associated with the gesture if any.

The return value is a btn = {"btn_id":{loc": loc, "action": ges}} all other values of the key, if any will not be carried forward.

where, loc = (x, y, w, h) of the gestured btn with action as one of the gesture values.

### methods touch_count() and touch_points()

These methods may be used for implementing multi touch capability presumably supported by FocalTouch.

For the hardware tested, it was not found reliable as a result the btn_gesture() method does not support it.

The Multi touch only recognizes changes in y coodinates but not sensitive to x coordinate diferences.

This may be verified in the test script for "touch_count" method as wells as "touch_points" method.

In otherwords, if the two fingers touching the screen lineup along x axis, then only one finger is registered.

However, this not the case if the two touch points are separated along y axis only.

### method touch_detected()

The method touch_detected(loc=(x, y, h, w)) with a default loc of (0, 0, 160, 120) returns True, False or None.

It is used to first find out which location (or btn) is touched before calling btn_gesture() method

