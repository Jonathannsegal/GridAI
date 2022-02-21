"""Imports"""


class CommandHandler():
    """Command Handler"""

    def __init__(self):
        self.commands = {
            "com.assistant.commands.VoltagePeakSpecific":
                CommandHandler.voltage_peak_specific,
            "com.assistant.commands.VoltageComparisonSpecific":
                CommandHandler.voltage_comparison_specific,
            "com.assistant.commands.NumberOf":
                CommandHandler.number_of,
        }

    def handle_command(self, command, input_args):
        """Handles incoming commands"""
        return self.commands[command](input_args)

    @staticmethod
    def voltage_peak_specific(input_args: dict):
        """Retrieves highest voltage for feeder_num."""
        feeder_num = input_args["feeder_num"]["value"]
        return feeder_num

    @staticmethod
    def voltage_comparison_specific(input_args: dict):
        """Retrieves the voltage for feeder_num which are within the specified range"""
        feeder_num = input_args["voltage"]["value"]
        return feeder_num

    @staticmethod
    def number_of(input_args: dict):
        """Retrieves the number of the specified object type"""
        object_type = input_args["object_type"]["key"]
        return object_type
