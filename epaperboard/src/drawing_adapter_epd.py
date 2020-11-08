from .drawing import DrawingAdapter
try:
    from IT8951 import constants
    from IT8951.display import AutoEPDDisplay
    has_it8951 = True
except ImportError:
    has_it8951 = False
import threading


class DrawingAdapterEPD(DrawingAdapter):
    def __init__(self, vcom: float):
        if has_it8951:
            print('Setting up the display using VCOM=' + str(vcom))
            self.display = AutoEPDDisplay(vcom=vcom, spi_hz=24000000)
            self.display.epd.wait_display_ready()
            self.display.clear()
        else:
            raise Exception("IT8951 driver not present")
        self.lock = threading.RLock()
        super().__init__(self.display.frame_buf)

    def draw(self):
        with self.lock:
            self.display.epd.run()
            self.display.draw_full(constants.DisplayModes.GC16)
            self.display.epd.wait_display_ready()
            self.display.epd.sleep()
