from assistant.src.assistant_service import *

def test_process_query():
    """Tests the AssistantService's process_query function"""
    service = AssistantService()
    queries = [
        ("Get the voltage peak on feeder 1234", ('com.assistant.commands.PeakSpecific', {
            'feature_type': {'key': 'VOLTAGE', 'value': 'voltage'},
            'feeder_num': {'key': 'INTEGER', 'value': '1234'}
        })),
        ("How many Transformers are in the system?", ('com.assistant.commands.NumberOf', {
            'object_type': {'key': 'TRANSFORMER', 'value': 'transformers'}
        })),
        ("Show voltages less than 1.03 p.u.", ('com.assistant.commands.Comparison', {
            'feeder_num': {'key': None, 'value': None},
            'feature_type': {'key': 'VOLTAGE', 'value': 'voltages'},
            'comparison_type': {'key': 'LESS', 'value': 'less than'},
            'comparison_value': {'key': 'FLOAT', 'value': '1.03'},
            'unit': {'key': 'PER_UNIT', 'value': 'p.u.'}
        })),
        ("Show voltages less than 100", ('com.assistant.commands.Comparison', {
            'feeder_num': {'key': None, 'value': None},
            'feature_type': {'key': 'VOLTAGE', 'value': 'voltages'},
            'comparison_type': {'key': 'LESS', 'value': 'less than'},
            'comparison_value': {'key': 'INTEGER', 'value': '100'},
            'unit': {'key': None, 'value': None}
        })),
        ("Get the top 10 values", ('com.assistant.commands.Extrema', {
            'extrema_type': {'key': 'MAX', 'value': 'top'},
            'object_type': {'key': None, 'value': None},
            'feature_type': {'key': 'DEFAULT', 'value': 'value'},
            'count': {'key': 'INTEGER', 'value': '10'}
        })),
        ("Get the top 10 voltages", ('com.assistant.commands.Extrema', {
            'extrema_type': {'key': 'MAX', 'value': 'top'},
            'object_type': {'key': None, 'value': None},
            'feature_type': {'key': 'VOLTAGE', 'value': 'voltage'},
            'count': {'key': 'INTEGER', 'value': '10'}
        })),
        ("Get the rate of change for voltages", ('com.assistant.commands.RateOfChange', {
            'rate_of_change': {'key': 'RATE_OF_CHANGE', 'value': 'rate of change'},
            'object_type': {'key': None, 'value': None},
            'feature_type': {'key': 'VOLTAGE', 'value': 'voltage'}
        })),
        ("How many BUGS are in the system?", (None, None)),
    ]
    for command, expected_return in queries:
        ret = service.process_query(command)
        assert ret[0] == expected_return[0]
        assert ret[1] == expected_return[1]
