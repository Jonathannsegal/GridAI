"""Imports"""
import json
import os


def aggregate_jsons(path):
    """Generates a dictionary object using jsons objects using the descendants of a directory"""

    commands_dict = {}
    files = os.listdir(path)
    for file in files:
        filepath = os.path.join(path, file)
        if os.path.isdir(filepath):
            json_dict = aggregate_jsons(filepath)
            base_split = file.split('.')
            key = base_split[0]
            commands_dict[key] = list(json_dict.values())
        else:
            base_split = file.split('.')
            if base_split[-1] == "json":
                with open(filepath, "r", encoding='utf-8') as f:
                    key = base_split[0]
                    value = json.load(f)
                    commands_dict[key] = value
    return commands_dict


def create_actions_json():
    """Generates the action.json file"""
    src_dir = os.path.dirname(os.path.realpath(__file__))
    commands_path = os.path.join(src_dir, "custom_commands")
    json_dict = aggregate_jsons(commands_path)

    actions_path = os.path.join(src_dir, "actions.json")
    with open(actions_path, "w+", encoding='utf-8') as f:
        pretty_json = json.dumps(json_dict, indent=4)
        f.write(pretty_json)


if __name__ == "__main__":
    create_actions_json()
