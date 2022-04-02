"""Imports"""
import json
import os
import re


class AssistantService():
    """AssistantService"""

    def __init__(self):
        self.actions = None
        filepath = os.path.join(os.path.dirname(__file__), "actions.json")
        with open(filepath, "r", encoding='utf-8') as f:
            self.actions = json.load(f)
        self.types = {action_type["name"]: action_type for action_type in self.actions["types"]}

    def process_query(self, query: str):
        """Processes the text query"""
        query = query.lower().lstrip().rstrip()
        for stop_word in self.actions["stop_words"]:
            query = query.replace(f' {stop_word} ', " ")

        for action in self.actions["actions"]:
            res = self.check_action_for_query(action["intent"], query)
            if res:
                responses = action["fulfillment"]["staticFulfillment"]["templatedResponse"]["items"]
                for response_item in responses:
                    for key in response_item:
                        if key == "simpleResponse":
                            pass
                        elif key == "deviceExecution":
                            handler = response_item[key]["command"]
                            input_args = {
                                param: res[response_item[key]["params"][param][1:]]
                                for param in response_item[key]["params"]
                            }
                            return (handler, input_args)

        return (None, None)

    def check_action_for_query(self, action_intent, query):
        """Checks the query to see if its structure matches with the given action."""
        parameters = action_intent["parameters"]
        patterns = action_intent["trigger"]["queryPatterns"]

        for pattern in patterns:
            regex, param_positions = self.create_pattern_regex(pattern, parameters)
            match = regex.match(query)

            if match:
                param_results = self.format_match_results(match, param_positions, parameters)
                return param_results
        return None

    def create_pattern_regex(self, pattern, parameters):
        """Creates a regex string to check for this pattern"""
        pattern = str(pattern)
        param_str_positions = [
            {
                "start": None,
                "end": None,
                "type": "",
                "name": "",
            } for _ in parameters
        ]
        for i, param in enumerate(parameters):
            param_str = f'${param["type"]}:{param["name"]}'

            pos = pattern.find(param_str)
            param_str_positions[i]["start"] = pos
            param_str_positions[i]["end"] = pos + len(param_str)
            param_str_positions[i]["type"] = param["type"]
            param_str_positions[i]["name"] = param["name"]

        param_str_positions = sorted(param_str_positions, key=lambda param: param["start"])
        for i in reversed(range(len(param_str_positions))):
            param = param_str_positions[i]
            if param["start"] < 0:
                continue

            param_regex_str = self.construct_param_regex_str(param)

            start = param["start"]
            end = param["end"]
            # Create major capture group for this feature
            param_regex_str = f'({param_regex_str})'

            # Note: does not support the use of identical parameter variables
            # If needed, handle this enforcement logic in custom command handler
            pattern = pattern[:start] + param_regex_str + pattern[end:]

        pattern = pattern.lower()
        # pattern.replace(" ", "\w?")
        return re.compile(pattern), param_str_positions

    def construct_param_regex_str(self, param):
        """
        Constructs a param regex string out of the entities and their synonyms
        for that parameter
        """
        entities_str = ""
        param_type = self.types[f'${param["type"]}']
        for entity_ind in range(len(param_type["entities"])):
            entity = param_type["entities"][entity_ind]
            synonyms_str = ""
            for synonym in entity["synonyms"]:
                synonyms_str += f'(?:{synonym})|'
            entities_str += f'({synonyms_str[:-1]})|'
        entities_str = entities_str[:-1]
        return entities_str

    def format_match_results(self, match, param_positions, parameters):
        """
        Formats a regex match result by identifying its valid groups and storing them for input use
        by the command handler.
        """
        param_results = {
            param["name"]: {
                "key": None,
                "value": None
            } for param in parameters
        }
        missing_params = {
            param["name"] for param in param_positions if param["start"] < 0
        }

        group_ind = 1
        for param in param_positions:
            param_res = param_results[param["name"]]
            param_type = self.types[f'${param["type"]}']
            if param["name"] in missing_params:
                continue
            if match.group(group_ind):
                param_res["value"] = match.group(group_ind).lstrip(' ').rstrip(' ')
                group_ind += 1
                for entity_ind in range(len(param_type["entities"])):
                    entity = param_type["entities"][entity_ind]
                    if match.group(group_ind):
                        param_res["key"] = entity["key"]
                        group_ind += len(param_type["entities"]) - entity_ind
                        break
                    group_ind += 1
            else:
                group_ind += len(param_type["entities"])

        return param_results
