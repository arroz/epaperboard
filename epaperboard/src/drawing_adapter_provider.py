from .drawing import DrawingAdapter, DevDrawingAdapter
from .drawing_adapter_epd import DrawingAdapterEPD
from .config import Config
from .drawing_adapter_type import DrawingAdapterType
import sys


def drawing_adapter_for(adapter_type: DrawingAdapterType, config: Config) -> DrawingAdapter:
    if adapter_type == DrawingAdapterType.DEV:
        return DevDrawingAdapter()
    elif adapter_type == DrawingAdapterType.EPD:
        if config.has_epd_vcom():
            return DrawingAdapterEPD(config.epd_vcom())
        else:
            print("VCOM not defined. To use the e-paper display, the config file must have an entry called 'epd_vcom' "
                  "with the VCOM value. Check the documentation for more details.", file=sys.stderr)
            exit(1)
