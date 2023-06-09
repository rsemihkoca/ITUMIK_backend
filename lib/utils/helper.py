import json
from pathlib import Path
desk_config_path = Path(__file__).resolve().parent.parent.parent / "desk-config.json"

def get_topic_name():
    with open(desk_config_path, 'r') as file:
        data = json.load(file)
    floor_key = list(data.keys())[0]
    desk_key = list(data[floor_key].keys())[0]
    mqtt_topic = f"{floor_key}/{desk_key}"
    return mqtt_topic