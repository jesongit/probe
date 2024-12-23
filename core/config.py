import json
import datetime
from pathlib import Path

file = Path("setting.json")
time_format = "%Y-%m-%d %H:%M:%S"
CONFIG = json.loads(file.read_text())


def update_offset(send_offset, received_offset):
    CONFIG["time"] = datetime.datetime.now().strftime(time_format)
    CONFIG["send_offset"] = send_offset
    CONFIG["received_offset"] = received_offset
    print(f"send_offset: {send_offset}, received_offset: {received_offset}")
    write_file()


def update(**kwargs):
    CONFIG.update(kwargs)
    write_file()


def write_file():
    file.write_text(json.dumps(CONFIG))
