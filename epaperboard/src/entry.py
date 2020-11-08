import json
from enum import Enum
from datetime import datetime, timedelta


class State(Enum):
    OK = 0
    WARNING = 1
    CRITICAL = 2
    UNKNOWN = 3


class Entry:
    def __init__(self, key: str, state: State, message: str, date: datetime = None):
        self.key = key
        self.state = state
        self.message = message
        self.date = date if date is not None else datetime.now()

    def json(self):
        return {"key": self.key, "state": self.state.value, "message": self.message,
                "date": datetime.timestamp(self.date)}

    def decode_json(json):
        return Entry(json["key"], State(json["state"]), json["message"], datetime.fromtimestamp(json["date"]))

    def __str__(self):
        return self.key + ": " + self.state.name + " (" + self.message + ")"

    def is_too_old(self, ttl) -> bool:
        if ttl == 0:
            return False
        delta = timedelta(seconds=ttl)
        return self.date + delta < datetime.now()


class EntryManager:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.entries = self.entries_from_json()

    def entries_from_json(self) -> dict:
        try:
            with open(self.filepath, "r") as read_file:
                j = json.load(read_file)
                return {k: Entry.decode_json(v) for (k, v) in j.items()}
        except FileNotFoundError:
            print("File not found: " + self.filepath + ". Starting fresh.")
            return {}
        except IOError:
            print("Error loading file " + self.filepath)
            raise

    def add_entry(self, entry: Entry) -> bool:
        changed = True
        if entry.key in self.entries:
            previous_entry: Entry = self.entries[entry.key]
            same = previous_entry.state == entry.state and previous_entry.message == entry.message
            changed = not same
        self.entries[entry.key] = entry
        self.save_json()
        return changed

    def save_json(self):
        with open(self.filepath, "w") as write_file:
            json.dump(self, write_file, cls=EntryManagerEncoder)

    def __str__(self):
        return self.entries.__str__()


class EntryManagerEncoder(json.JSONEncoder):
    def default(self, o: EntryManager):
        return {k: v.json() for (k, v) in o.entries.items()}
