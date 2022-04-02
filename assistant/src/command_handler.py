"""Imports"""
import requests


def default(val, default_value):
    """Replaces val if it is None"""
    return default_value if val is None else val


class CommandHandler():
    """Command Handler"""

    def __init__(self):
        self.commands = {
            "com.assistant.commands.PeakSpecific":
                CommandHandler.peak_specific,
            "com.assistant.commands.Comparison":
                CommandHandler.comparison,
            "com.assistant.commands.Extrema":
                CommandHandler.extrema,
            "com.assistant.commands.RateOfChange":
                CommandHandler.rate_of_change,
            "com.assistant.commands.NumberOf":
                CommandHandler.number_of,
        }

    def handle_command(self, command, input_args):
        """Handles incoming commands"""
        return self.commands[command](input_args)

    @staticmethod
    def peak_specific(input_args: dict):
        """Retrieves highest feature value for feeder_num."""
        feeder_num = input_args["feeder_num"]["value"]
        feature_type = default(input_args["feature_type"]["key"], "DEFAULT")
        return feeder_num, feature_type

    @staticmethod
    def comparison(input_args: dict):
        """Retrieves the voltage for feeder_num which are within the specified range"""
        comparison_type = input_args["comparison_type"]["key"]
        comparison_value = input_args["comparison_value"]["value"]

        unit = default(input_args["unit"]["key"], "DEFAULT")
        feature_type = default(input_args["feature_type"]["key"], "DEFAULT")
        feeder_num = default(input_args["feeder_num"]["value"], None)

        return requests.get(
            url="https://data-influx-kxcfw5balq-uc.a.run.app/comparison",
            params={
                "comparison_type":
                    1 if comparison_type == "LESS" else
                    2 if comparison_type == "GREATER" else
                    3,
                "comp_val": comparison_value,
                "power_type": feature_type,
                "busId": feeder_num,
                "unit": unit,
            }
        )
        # return comparison_type, comparison_value, units, feature_type, feeder_num

    @staticmethod
    def extrema(input_args: dict):
        """Retrieves the top or lowest values of a feature for objects of object_type"""
        extrema_type = input_args["extrema_type"]["key"]
        count = default(input_args["count"]["value"], 0)

        object_type = default(input_args["object_type"]["key"], "DEFAULT")
        feature_type = default(input_args["feature_type"]["key"], "DEFAULT")

        return extrema_type, count, object_type, feature_type

    @staticmethod
    def rate_of_change(input_args: dict):
        """Calculates the rate of change in a feature for target objects"""
        object_type = default(input_args["object_type"]["key"], "DEFAULT")
        feature_type = default(input_args["feature_type"]["key"], "DEFAULT")

        return object_type, feature_type

    @staticmethod
    def number_of(input_args: dict):
        """Retrieves the number of the specified object type"""
        object_type = input_args["object_type"]["key"]
        return object_type
