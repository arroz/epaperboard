from epaperboard.src.entry import EntryManager
from epaperboard.src.config import Config
from epaperboard.src.drawing import Drawer
from epaperboard.src.drawing_adapter_provider import drawing_adapter_for
from epaperboard.src.server import Server
import argparse


def run():
    parser = argparse.ArgumentParser(description='Paperboard')
    parser.add_argument(dest='config_file_path', type=str, help='path to the config file')
    args = parser.parse_args()

    config = Config(args.config_file_path)
    entry_manager = EntryManager(config.data_file_path())
    dashboard = config.dashboard(entry_manager)
    adapter = drawing_adapter_for(config.drawing_adapter_type())
    drawer = Drawer(adapter, dashboard)
    drawer.draw_full(True)

    server = Server(drawer, entry_manager, config.server_port())
    server.run()


if __name__ == "__main__":
    run()
