from assistant.src.command_handler import *

def test_peak_specific():
    """Test the PeakSpecific command"""
    ret = CommandHandler.peak_specific({
        'feature_type': {'key': 'VOLTAGE', 'value': 'voltage'},
        'feeder_num': {'key': 'INTEGER', 'value': '1234'}
    })

def test_comparison():
    """Test the Comparison command"""
    ret = CommandHandler.comparison({
        'feeder_num': {'key': None, 'value': None},
        'feature_type': {'key': 'VOLTAGE', 'value': 'voltages'},
        'comparison_type': {'key': 'LESS', 'value': 'less than'},
        'comparison_value': {'key': 'FLOAT', 'value': '1.03'},
        'unit': {'key': 'PER_UNIT', 'value': 'p.u.'}
    })
    ret = CommandHandler.comparison({
        'feeder_num': {'key': None, 'value': None},
        'feature_type': {'key': 'VOLTAGE', 'value': 'voltages'},
        'comparison_type': {'key': 'LESS', 'value': 'less than'},
        'comparison_value': {'key': 'INTEGER', 'value': '100'},
        'unit': {'key': None, 'value': None}
    })

def test_extrema():
    """Test the Extrema command"""
    ret = CommandHandler.extrema({
        'extrema_type': {'key': 'MAX', 'value': 'top'},
        'object_type': {'key': None, 'value': None},
        'feature_type': {'key': 'DEFAULT', 'value': 'value'},
        'count': {'key': 'INTEGER', 'value': '10'}
    })

def test_rate_of_change():
    """Test the RateOfChange command"""
    ret = CommandHandler.rate_of_change({
        'rate_of_change': {'key': 'RATE_OF_CHANGE', 'value': 'rate of change'},
        'object_type': {'key': None, 'value': None},
        'feature_type': {'key': 'VOLTAGE', 'value': 'voltage'}
    })

def test_number_of():
    """Test the NumberOf command"""
    ret = CommandHandler.number_of({
        "name": "Query_NumberOf",
        "params": {
            "object_type": {
                "original": "transformers",
                "resolved": "TRANSFORMER"
            }
        },
        "query": "Get the number of transformers."
    })

def test_handle_command():
    """Test the handle_command command"""
    ret = CommandHandler.handle_command("number_of", {
        "name": "Query_NumberOf",
        "params": {
            "object_type": {
                "original": "transformers",
                "resolved": "TRANSFORMER"
            }
        },
        "query": "Get the number of transformers."
    })

def test_default():
    """Test the default command"""
    ret = default(None, -1)
    assert ret == -1
    ret = default(2, -1)
    assert ret == 2

def test_handle_webhook():
    """Test the generic webhook"""
    request = {
        "handler": {
      "name": "generic_query"
    },
    "intent": {
      "name": "Query_Generic",
      "params": {
        "feature": {
          "original": "active power",
          "resolved": "ACTIVE_POWER"
        },
        "extrema": {
          "original": "top",
          "resolved": "MAX"
        }
      },
      "query": "get the top active power"
    },
    "scene": {
      "name": "mainScene",
      "slotFillingStatus": "UNSPECIFIED",
      "slots": {},
      "next": {
        "name": "mainScene"
      }
    },
    "session": {
      "id": "ABwppHETS9xzMOT2cyZ-crMcfpmowmukQLF-o7-0Tgn-KES5bvrnNSu2p1WX_-Ob5ZqQEv21jt7bIIfe",
      "params": {},
      "typeOverrides": [],
      "languageCode": ""
    },
    "user": {
      "locale": "en-US",
      "params": {},
      "accountLinkingStatus": "ACCOUNT_LINKING_STATUS_UNSPECIFIED",
      "verificationStatus": "VERIFIED",
      "packageEntitlements": [],
      "gaiamint": "",
      "permissions": [],
      "lastSeenTime": "2022-04-27T20:33:04Z"
    },
    "home": {
      "params": {}
    },
    "device": {
      "capabilities": [
        "SPEECH",
        "RICH_RESPONSE",
        "LONG_FORM_AUDIO"
      ],
      "timeZone": {
        "id": "America/Chicago",
        "version": ""
      }
    }
    }
    ret = CommandHandler.handle_webhook(request)
