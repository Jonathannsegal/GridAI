from assistant.src.app import *

def test_process_query():
    """Tests the AssistantService's process_query function"""
    service = AssistantService()
    res = service.process_query("Get the voltage peak on feeder 1234")
    assert res == "1234"
    res = service.process_query("How many Transformers are in the system?")
    assert res == "TRANSFORMER"
    res = service.process_query("Show voltages less than 1.03 p.u. on feeder 1234?")
    assert res == "1.03 p.u."
    res = service.process_query("How many BUGS are in the system?")
    assert res is None
