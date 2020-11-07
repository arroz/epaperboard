from bottle import request, run, Bottle
from .entry import State, Entry, EntryManager
from .drawing import Drawer


class Server:
    def __init__(self, drawer: Drawer, entry_manager: EntryManager, port: int):
        self.port = port
        self.app = Bottle()
        self.drawer = drawer
        self.entry_manager = entry_manager
        self.route()

    def route(self):
        self.app.route('/entry/<entry_name>', method='POST', callback=self.add_entry)
        self.app.route('/update', method='POST', callback=self.update)
        self.app.route('/redraw', method='POST', callback=self.redraw)

    def add_entry(self, entry_name):
        state_name = request.forms.get('state', default="UNKNOWN")
        message = request.forms.get('message', default="")
        state = State[state_name]
        entry = Entry(entry_name, state, message)
        self.entry_manager.add_entry(entry)
        self.drawer.draw_full(False)

    def update(self):
        self.drawer.draw_full(False)

    def redraw(self):
        self.drawer.draw_full(True)

    def run(self):
        run(self.app, host='0.0.0.0', port=self.port)

