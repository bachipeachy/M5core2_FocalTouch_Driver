import time
import axp202c
from focaltouch import FocalTouch
from machine import SoftI2C, Pin


class FocalTouchTest:
    """ test FocalTouch capacitive touch sensor """

    def __init__(self, n=10):

        self.n = n
        i2c = self.init_m5core2()
        self.ft = FocalTouch(i2c, btns={"topleft_quad": {'loc': (0, 0, 160, 120), 'lbl': 'TLQ'},
                                        "botright_quad": {'loc': (160, 120, 160, 120)}}, debug=False)
        self.run()

    @staticmethod
    def init_m5core2():
        # initialize M5Stack Core2 to power-up and communicate with FocalTouch

        i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
        axp = axp202c.PMU(i2c, address=0x34)
        axp.enablePower(axp202c.AXP192_LDO2)
        axp.setDC3Voltage(3000)
        return i2c

    def touch_count_test(self):
        print("touch with one or two fingers\ntest runs for {} interations ..".format(self.n))

        i = 0
        while i < self.n:
            count = self.ft.touch_count
            if 0 < count < 3:
                print("{}>ft.touch_count -> {}".format(i + 1, count))
                i = i + 1
                time.sleep_ms(200)

    def touch_points_test(self):
        print("touch with one or two fingers\ntest runs for {} interations ..".format(self.n))
        tps_prev = None
        i = 0
        while i < self.n:
            tps = self.ft.touch_points
            if tps_prev != tps:
                print("{}>ft.touches -> {}".format(i + 1, tps))
                tps_prev = tps
                i = i + 1
                time.sleep_ms(200)

    def touch_detected_test(self):
        print("TOUCHES IN or OUT top-left quadrant\ntest runs for {} interations ..".format(self.n))
        val_prev = None
        i = 0
        loc = (0, 0, 160, 120)
        while i < self.n:
            val = self.ft.touch_detected(loc=loc)
            if val_prev != val:
                print("{}>ft.touch_detected at -{} {}".format(i + 1, loc, val))
                val_prev = val
                i = i + 1
                time.sleep_ms(200)

    def btn_gesture_test(self):
        touchctr = 8
        print("btn_gesture test runs for {} iterations ..\n"
              "on configured btns TAP, HOLD or swipe LEFT, RIGHT, UP or DOWN ..".format(touchctr))
        print("Two configured btns are:  topleft_qud and botright_quad")

        for i in range(touchctr):
            print(i + 1, end='')
            while self.ft.btn_gesture() is None:
                pass
        print("exiting btn_gesture_test ..")

    def run(self):
        print("Default params for initializing FocalTouch class object ft ..\n"
              "ft.btns={}, debug={}\n"
              "ft.touched_th={}, ft.held_th={}, ft.delta_x_th={}, ft.delta_y_th={}".format
              (self.ft.btns, self.ft.debug, self.ft.touched_th, self.ft.held_th, self.ft.delta_x_th,
               self.ft.delta_y_th))

        print("\nTest runs for {} iterations ...".format(self.n))
        print("TAP, HOLD or SWIPE the touch screen topleft_quad or botright_quad ..\n")

        ch = input("Enter..\n"
                   " 1 for 'touch_count' method\n"
                   " 2 for 'touch_points' method\n"
                   " 3 for 'touch_detected method\n"
                   " 4 for 'btn_gesture' method\n")

        try:
            if ch == '1':
                self.touch_count_test()
            elif ch == '2':
                self.touch_points_test()
            elif ch == '3':
                self.touch_detected_test()
            elif ch == '4':
                self.btn_gesture_test()
            print("goodbye ..")

        except Exception as e:
            print(" oops I blew up ..", e)


if __name__ == "__main__":
    FocalTouchTest(n=10)
