import os

from assistant.src.create_actions_json import *

def test_aggregate_jsons():
    """Tests a the json file aggregator"""
    aggregate_jsons(os.path.join(os.path.dirname(os.path.dirname(__file__)), "src", "custom_commands"))
