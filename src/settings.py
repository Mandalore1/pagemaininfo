import json

with open("settings.json", "r") as file:
    settings_json = json.load(file)

TAGS_TO_SEARCH = settings_json["tags_to_search"]
LINE_WIDTH = settings_json["line_width"]
