import json
from .drawing_adapter_provider import DrawingAdapterType
from .dashboard import Dashboard, DashboardElement
from .entry import EntryManager


class Config:
    def __init__(self, config_file_path):
        with open(config_file_path, "r") as read_file:
            self.config = json.load(read_file)

    def server_port(self) -> int:
        return self.config['server_port']

    def data_file_path(self) -> str:
        return self.config['data_file_path']

    def drawing_adapter_type(self) -> DrawingAdapterType:
        type_name = self.config['drawing_adapter_type']
        return DrawingAdapterType[type_name]

    def dashboard(self, entry_manager: EntryManager) -> Dashboard:
        elements = list(map(lambda element: Config.dashboard_element(element), self.config['dashboard']))
        return Dashboard(entry_manager, elements)

    @staticmethod
    def dashboard_element(json_element) -> DashboardElement:
        return DashboardElement(
            json_element['title'],
            json_element['keys'],
            json_element['ok_string'] if 'ok_string' in json_element else "OK",
            json_element['warning_string'] if 'warning_string' in json_element else "Warning",
            json_element['critical_string'] if 'critical_string' in json_element else "Critical",
            json_element['unknown_string'] if 'unknown_string' in json_element else "Unknown",
            json_element['ttl'] if 'ttl' in json_element else 0
        )
