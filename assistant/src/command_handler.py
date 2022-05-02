"""Imports"""
from datetime import datetime, timedelta, timezone
from warnings import warn
import requests

INFLUX_URL = "https://data-influx-kxcfw5balq-uc.a.run.app"
NEO4J_URL = "https://data-neo4j-kxcfw5balq-uc.a.run.app"


def default(val, default_value):
    """Replaces val if it is None"""
    return default_value if val is None else val


class CommandHandler():
    """Command Handler"""

    @staticmethod
    def handle_webhook(query_result: dict) -> dict:
        """Handles incoming commands
        
        A dictionary object is be returned.
        This dictionary is formated as a "prompt" with the structure presented here:
        https://developers.google.com/assistant/conversational/webhooks#example-response.

        For more prompt formats, look at https://developers.google.com/assistant/conversational/prompts.
        """
        handler = query_result["handler"]["name"]
        return CommandHandler.commands[handler](query_result["intent"])

    @staticmethod
    def generic_query(intent: dict) -> dict:  # noqa: C901; pylint: disable=R0914,R0912,R0915
        """Execute a generic query.
        Once example of such a query is as follows:
        - Get the top 3 active powers above 3 and under 5 volts between April 25th and April 27th.
        """
        args = intent["params"]
        params = {}
        response_str = "Showing"

        if "extrema" in args:
            extrema = args["extrema"]["resolved"]
            params["extrema_type"] = extrema
            raw = "top" if extrema == "MAX" else \
                  "bottom"
            response_str += f" {raw}"

        if "count" in args:
            params["count"] = args["count"]["resolved"]
            raw = args["count"]["resolved"]
            response_str += f" {raw}"

        if "feature" in args:
            feature = args["feature"]["resolved"]
            words = feature.lower().split('_')
            feature_camal_case = words[0] + ''.join(word.title() for word in words[1:])
            params["power_type"] = feature_camal_case
            raw = args["feature"]["original"]
            response_str += f" {raw}"

        if "range_values" in args:
            value_strings = args["range_values"]["resolved"]
            min_val = None
            max_val = None
            for value_str in value_strings:
                words = set(value_str.split())
                nums = [float(word) for word in words if word.isnumeric()]
                if len(value_strings) == 1:
                    num = nums[0]
                    if any(comp in words for comp in ["under", "below", "less", "lower"]):
                        if max_val is None or num > max_val:
                            max_val = num
                    elif any(comp in words for comp in ["over", "above", "greater", "higher"]):
                        if min_val is None or num > min_val:
                            min_val = num
                else:
                    for num in nums:
                        if max_val is None or num > max_val:
                            max_val = num
                        if min_val is None or num < min_val:
                            min_val = num

            if min_val:
                params["lowest_value"] = min_val
            if max_val:
                params["highest_value"] = max_val
            if min_val and max_val:
                response_str += f" between {min_val} and {max_val}"
            elif min_val:
                response_str += f" above {min_val}"
            elif max_val:
                response_str += f" under {max_val}"

        if "times" in args:
            times = args["times"]["resolved"]
            reftime = datetime.now()
            if len(times) == 1:
                time = times[0]
                curdate = datetime(
                    year=time.get("year", reftime.year),
                    month=time.get("month", reftime.month),
                    day=time.get("day", reftime.day),
                    hour=time.get("hour", reftime.hour),
                    minute=time.get("minute", reftime.minute),
                )

                comparators = args["time_comparator"]["resolved"]
                comparator = "ON" if len(comparators) < 1 else comparators[0]
                if comparator == "AT":
                    delta = timedelta(minutes=30)
                    params["start"] = curdate - delta
                    params["stop"] = curdate + delta
                if comparator == "ON":
                    delta = timedelta(days=1) - timedelta(microseconds=1)
                    params["start"] = curdate.replace(hour=0, minute=0, second=0, microsecond=0)
                    params["stop"] = params["start"] + delta
                elif comparator == "BEFORE":
                    params["stop"] = curdate
                elif comparator == "AFTER":
                    params["start"] = curdate
            else:
                min_date = None
                max_date = None
                for time in times:
                    for measure in ["year", "month", "day", "hour", "minute", "second"]:
                        if measure in time:
                            reftime = reftime.replace(**{measure: time[measure]})

                for time in times:
                    curdate = datetime(
                        year=time.get("year", reftime.year),
                        month=time.get("month", reftime.month),
                        day=time.get("day", reftime.day),
                        hour=time.get("hour", reftime.hour),
                        minute=time.get("minute", reftime.minute),
                    )
                    if min_date is None or curdate < min_date:
                        min_date = curdate
                    if max_date is None or curdate > max_date:
                        max_date = curdate

                params["start"] = min_date
                params["stop"] = max_date

            for date_name in ["start", "stop"]:
                if date_name in params:
                    date = params[date_name]
                    # # Set time zone
                    date = date.replace(tzinfo=timezone(timedelta(hours=0)))
                    params[date_name] = date.isoformat()
                    format_str = "%m-%d-%y %H:%M:%S"
                    if date_name == "start":
                        response_str += f" after {date.strftime(format_str)}"
                    elif date_name == "stop":
                        if "start" in params and "stop" in params:
                            response_str += " and"
                        response_str += f" before {date.strftime(format_str)}"

        response_str += "."
        response = requests.get(
            url=INFLUX_URL+"/generic",
            params=params
        )
        table = response.json()

        title = "Voltages"
        if "feature" in args:
            feature = args["feature"]["resolved"]
            words = feature.split('_')
            title = ' '.join(word.title() for word in words)

        headers = table[0]
        rows = table[1:]

        prompt = {
            "override": False,
            "firstSimple": {
                "speech": response_str,
                "text": response_str,
            },
            "content": {
                "table": {
                    "button": {},
                    "columns": [
                        {"header": col} for col in headers
                    ],
                    "rows": [
                        {
                            "cells": [
                                {
                                    "text": str(col_data)
                                } for col_data in row
                            ]
                        } for row in rows
                    ],
                    "title": title
                }
            }
        }
        return prompt

    @staticmethod
    def number_of(intent: dict) -> dict:
        """Retrieves the number of the specified object type"""
        args = intent["params"]
        object_type = args["object_type"]["resolved"]

        # TODO: Process the object_type to fit that which is stored in the database.
        #        This could be done in Actions on Google.

        response = requests.get(
            url=NEO4J_URL+"/getNodesByType",
            params={"type": object_type}
        )

        num = len(response.json()) - 1
        text_response = f"There are {num} {object_type.lower()}s."
        prompt = {
            "override": False,
            "firstSimple": {
                "speech": text_response,
                "text": text_response
            }
        }
        return prompt

    @staticmethod
    def handle_command(command, input_args):
        """Handles incoming commands"""
        warn("handle_command function is now deprecated.")

        return CommandHandler.commands[command](input_args)

    @staticmethod
    def peak_specific(input_args: dict):
        """Retrieves highest feature value for feeder_num."""
        warn("peak_specific function is now deprecated.")

        feeder_num = input_args["feeder_num"]["value"]
        feature_type = default(input_args["feature_type"]["key"], "DEFAULT")
        return feeder_num, feature_type

    @staticmethod
    def comparison(input_args: dict):
        """Retrieves the voltage for feeder_num which are within the specified range"""
        warn("comparison function is now deprecated.")

        comparison_type = input_args["comparison_type"]["key"]
        comparison_value = input_args["comparison_value"]["value"]

        unit = default(input_args["unit"]["key"], "DEFAULT")
        feature_type = default(input_args["feature_type"]["key"], "DEFAULT")
        feeder_num = default(input_args["feeder_num"]["value"], None)

        response = requests.get(
            url=INFLUX_URL+"/comparison",
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
        return response.json()

    @staticmethod
    def extrema(input_args: dict):
        """Retrieves the top or lowest values of a feature for objects of object_type"""
        warn("extrema function is now deprecated.")

        extrema_type = input_args["extrema_type"]["key"]
        count = default(input_args["count"]["value"], 0)

        object_type = default(input_args["object_type"]["key"], "DEFAULT")
        feature_type = default(input_args["feature_type"]["key"], "DEFAULT")

        response = requests.get(
            url=INFLUX_URL+"/getExtreme",
            params={
                "extrema_type": extrema_type,
                "count": count,
                "object_type": object_type,
                "feature_type": feature_type,
            }
        )
        return response.json()

    @staticmethod
    def rate_of_change(input_args: dict):
        """Calculates the rate of change in a feature for target objects"""
        warn("rate_of_change function is now deprecated.")

        object_type = default(input_args["object_type"]["key"], "DEFAULT")
        feature_type = default(input_args["feature_type"]["key"], "DEFAULT")

        return object_type, feature_type

    commands = {
        "com.assistant.commands.PeakSpecific":
            peak_specific.__func__,  # type: ignore
        "com.assistant.commands.Comparison":
            comparison.__func__,  # type: ignore
        "com.assistant.commands.Extrema":
            extrema.__func__,  # type: ignore
        "com.assistant.commands.RateOfChange":
            rate_of_change.__func__,  # type: ignore
        "number_of":
            number_of.__func__,  # type: ignore
        "generic_query":
            generic_query.__func__,  # type: ignore
    }
