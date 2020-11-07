from .entry import Entry, EntryManager, State


class Dashboard:
    def __init__(self, entry_manager: EntryManager, elements: list):
        self.elements = elements
        self.entry_manager = entry_manager

    def states(self):
        em = self.entry_manager
        return list(map(lambda e: (e, e.state(em)), self.elements))


class DashboardState:
    def __init__(self, state: State, state_description: str, message: str):
        self.state = state
        self.state_description = state_description
        self.message = message

    def __str__(self):
        msg = ": " + self.message if len(self.message) > 0 else ""
        return self.state_description + msg

    def __eq__(self, other):
        if isinstance(other, DashboardState):
            return self.state == other.state and self.state_description == other.state_description and self.message == other.message
        return False


class DashboardElement:
    def __init__(self, title: str,
                 keys: list,
                 ok_string: str = "OK",
                 warning_string: str = "Warning",
                 critical_string: str = "Error",
                 unknown_string: str = "Unknown",
                 ttl=0):
        if len(keys) == 0:
            raise Exception("Keys array must not be empty.")
        self.title = title
        self.keys = keys
        self.ttl = ttl
        self.state_descriptions = [ok_string, warning_string, critical_string, unknown_string]

    def state(self, entity_manager: EntryManager) -> DashboardState:
        key_state: State = State.OK
        message: str = ""
        for key in self.keys:
            spacer = "" if len(message) == 0 else " "
            if key in entity_manager.entries:
                entry: Entry = entity_manager.entries[key]
                if entry.is_too_old(self.ttl):
                    key_state = State.UNKNOWN
                    message += spacer + "[" + key + "] Timed out"
                else:
                    key_state = State(max(key_state.value, entry.state.value))
                    if len(entry.message) > 0:
                        message += spacer + "[" + key + "] " + entry.message
            else:
                key_state = State.UNKNOWN
                message += spacer + "[" + key + "] Unknown status."
        return DashboardState(key_state, self.state_descriptions[key_state.value], message)


