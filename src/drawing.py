from .dashboard import Dashboard, DashboardState, DashboardElement
from PIL import Image, ImageDraw, ImageFont
from abc import ABC, abstractmethod
import datetime
import threading
import subprocess

class DrawingAdapter(ABC):
    def __init__(self, image: Image):
        self.image = image

    def draw(self):
        pass


class DevDrawingAdapter(DrawingAdapter):
    def __init__(self):
        super().__init__(Image.new('L', (800, 600), 255))

    def draw(self):
        self.image.show()


class Drawer:
    def __init__(self, drawing_adapter: DrawingAdapter, dashboard: Dashboard):
        self.drawing_adapter = drawing_adapter
        self.dashboard = dashboard
        self.images_per_state = ["OK.png", "Warning.png", "Critical.png", "Unknown.png"]
        self.text_colors_per_state = [0, 0, 255, 0]
        self.lock = threading.RLock()
        self.previous_states = None
        self.bold_font = 'fonts/PTSans-Bold.ttf'
        self.regular_font = 'fonts/PTSans-Regular.ttf'

    def draw_full(self, force: bool):
        with self.lock:
            context = ImageDraw.Draw(self.drawing_adapter.image)
            context.rectangle([(0, 0), (800, 600)], fill=255)
            state_tuples = self.dashboard.states()
            states = list(map(lambda e: e[1], state_tuples))
            if (not force) and self.previous_states is not None and self.previous_states == states:
                return
            self.previous_states = states
            for row in range(2):
                for column in range(4):
                    index = row * 4 + column
                    coordinate = (200 * column, 200 * row)
                    if index < len(state_tuples):
                        self.draw(state_tuples[index], coordinate, context)
                    else:
                        self.draw_blank(coordinate, context)
            self.draw_text_area(context, state_tuples)
            self.draw_footer(context)
            self.drawing_adapter.draw()

    def draw(self, state_tuple: (DashboardElement, DashboardState), coordinate: (int, int), context: ImageDraw):
        element = state_tuple[0]
        state = state_tuple[1]
        icon = Image.open("images/" + self.images_per_state[state.state.value]).convert('L')
        self.drawing_adapter.image.paste(icon, box=coordinate)
        font = ImageFont.truetype(self.regular_font, 28)
        self.draw_centered_text((coordinate[0], coordinate[1] + 150), 200, element.title, font, context, 0)

    def draw_centered_text(self, coordinate: (int, int), max_width: int, text: str, font: ImageFont, context: ImageDraw,
                           fill: int):
        size = context.textsize(text, font=font)
        if size[0] > max_width:
            raise Exception("Text doesn't fit the box")
        coord = coordinate[0] + (max_width - size[0]) / 2
        context.text((coord, coordinate[1]), text, font=font, fill=fill)

    def draw_blank(self, coordinate: (int, int), context: ImageDraw):
        return

    def draw_footer(self, context: ImageDraw):
        context.rectangle([(0, 570), (800, 600)], fill=0)
        now = datetime.datetime.now()
        date_text = now.strftime("%b %d, %Y %H:%M:%S")
        font = ImageFont.truetype(self.bold_font, 20)
        context.text((5, 570), "Updated on " + date_text, font=font, fill=255)
        ip_addr = self.ip_address()
        size = context.textsize(ip_addr, font=font)
        context.text((800 - size[0] - 5, 570), ip_addr, font=font, fill=255)

    def draw_text_area(self, context: ImageDraw, states: [(DashboardElement, DashboardState)]):
        last_line_y = 410
        font = ImageFont.truetype(self.regular_font, 16)
        bold_font = ImageFont.truetype(self.bold_font, 16)
        for tuple in states:
            element = tuple[0]
            state = tuple[1]
            if len(state.message) > 0:
                header_size = context.textsize(element.title, font=bold_font)
                context.text((10, last_line_y), element.title, font=bold_font, fill=0)
                line = self.crop_line(state.message, font, 800 - header_size[0] - 20, context)
                context.text((14 + header_size[0], last_line_y), line, font=font, fill=0)
                last_line_y += header_size[1] + 4

    def crop_line(self, text: str, font: ImageFont, space: int, context: ImageDraw) -> str:
        if space <= 0:
            return ""
        if context.textsize(text, font=font)[0] < space:
            return text
        line = text[:300]  # truncate string to a reasonable size
        while True:
            line = line[:-1]
            if context.textsize(line + "…", font=font)[0] < space:
                return line + "…"
            if len(line) == 0:
                return ""

    def ip_address(self) -> str:
        result = subprocess.run(["/bin/hostname", "-I"], capture_output=True)
        return result.stdout.decode("utf-8")
