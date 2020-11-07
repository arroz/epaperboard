from .drawing import DrawingAdapter, DevDrawingAdapter
from .drawing_adapter_epd import DrawingAdapterEPD
from enum import Enum


class DrawingAdapterType(Enum):
    DEV = 0
    EPD = 1


def drawing_adapter_for(adapter_type: DrawingAdapterType) -> DrawingAdapter:
    if adapter_type == DrawingAdapterType.DEV:
        return DevDrawingAdapter()
    elif adapter_type == DrawingAdapterType.EPD:
        return DrawingAdapterEPD()