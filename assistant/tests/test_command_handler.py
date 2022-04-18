from assistant.src.command_handler import *

def test_peak_specific():
    """Test the PeakSpecific command"""
    handler = CommandHandler()
    ret = handler.peak_specific({
        'feature_type': {'key': 'VOLTAGE', 'value': 'voltage'},
        'feeder_num': {'key': 'INTEGER', 'value': '1234'}
    })

def test_comparison():
    """Test the Comparison command"""
    handler = CommandHandler()
    ret = handler.comparison({
        'feeder_num': {'key': None, 'value': None},
        'feature_type': {'key': 'VOLTAGE', 'value': 'voltages'},
        'comparison_type': {'key': 'LESS', 'value': 'less than'},
        'comparison_value': {'key': 'FLOAT', 'value': '1.03'},
        'unit': {'key': 'PER_UNIT', 'value': 'p.u.'}
    })
    ret = handler.comparison({
        'feeder_num': {'key': None, 'value': None},
        'feature_type': {'key': 'VOLTAGE', 'value': 'voltages'},
        'comparison_type': {'key': 'LESS', 'value': 'less than'},
        'comparison_value': {'key': 'INTEGER', 'value': '100'},
        'unit': {'key': None, 'value': None}
    })

def test_extrema():
    """Test the Extrema command"""
    handler = CommandHandler()
    ret = handler.extrema({
        'extrema_type': {'key': 'MAX', 'value': 'top'},
        'object_type': {'key': None, 'value': None},
        'feature_type': {'key': 'DEFAULT', 'value': 'value'},
        'count': {'key': 'INTEGER', 'value': '10'}
    })

def test_rate_of_change():
    """Test the RateOfChange command"""
    handler = CommandHandler()
    ret = handler.rate_of_change({
        'rate_of_change': {'key': 'RATE_OF_CHANGE', 'value': 'rate of change'},
        'object_type': {'key': None, 'value': None},
        'feature_type': {'key': 'VOLTAGE', 'value': 'voltage'}
    })

def test_number_of():
    """Test the NumberOf command"""
    handler = CommandHandler()
    ret = handler.number_of({
        'object_type': {'key': 'TRANSFORMER', 'value': 'transformers'}
    })

def test_handle_command():
    """Test the handle_command command"""
    handler = CommandHandler()
    ret = handler.handle_command("com.assistant.commands.NumberOf", {
        'object_type': {'key': 'TRANSFORMER', 'value': 'transformers'}
    })

def test_default():
    """Test the default command"""
    ret = default(None, -1)
    assert ret == -1
    ret = default(2, -1)
    assert ret == 2
