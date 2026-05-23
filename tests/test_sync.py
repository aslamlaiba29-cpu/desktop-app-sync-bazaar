# tests/test_sync.py
import json
from backend.sync import broker

def test_sync_broker_announcements():
    """Verify that events announced via broker are broadcasted to registered listeners."""
    # 1. Register listener queue
    q = broker.listen()
    assert len(broker.listeners) == 1

    # 2. Announce stock update event
    event_data = {"product_id": 42, "new_stock": 99}
    broker.announce("stock_update", event_data)

    # 3. Retrieve event message from queue
    message = q.get_nowait()
    assert message.startswith("data: ")
    
    # Extract json payload
    json_str = message.replace("data: ", "").strip()
    payload = json.loads(json_str)

    assert payload["type"] == "stock_update"
    assert payload["data"]["product_id"] == 42
    assert payload["data"]["new_stock"] == 99

    # 4. Clean up queue listener
    broker.remove_listener(q)
    assert len(broker.listeners) == 0
