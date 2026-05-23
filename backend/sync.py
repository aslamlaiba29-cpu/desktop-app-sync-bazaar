# backend/sync.py
"""Real-time synchronization broker using Server-Sent Events (SSE).
Allows broadcasting stock changes, order updates, and logs to all open clients in real-time.
"""

import queue
import json
import logging

class EventBroker:
    def __init__(self):
        self.listeners = []

    def listen(self):
        """Register a client queue listener."""
        q = queue.Queue(maxsize=50)
        self.listeners.append(q)
        return q

    def announce(self, event_type, data):
        """Announce an event to all connected listeners."""
        payload = {
            "type": event_type,
            "data": data
        }
        message = f"data: {json.dumps(payload)}\n\n"
        
        # Log the sync event to the logs file
        logging.info(f"Real-Time Sync Event [{event_type}]: {json.dumps(data)}")

        # Broadcast to all listeners
        for q in list(self.listeners):
            try:
                q.put_nowait(message)
            except queue.Full:
                # Remove stalled queue listener
                self.remove_listener(q)

    def remove_listener(self, q):
        """Unregister a client queue listener."""
        if q in self.listeners:
            self.listeners.remove(q)

broker = EventBroker()
