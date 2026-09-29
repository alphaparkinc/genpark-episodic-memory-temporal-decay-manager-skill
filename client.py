"""Episodic Memory Temporal Decay Manager.
100% Python Standard Library.
"""

import math
import time

class TemporalDecayMemory:
    """Manages memory retention and consolidation using Ebbinghaus forgetting curves."""
    def __init__(self, decay_rate=0.1):
        self.decay_rate = decay_rate
        self.memories = []

    def store(self, content, importance=1.0):
        self.memories.append({
            "content": content,
            "created_at": time.time(),
            "importance": importance,
            "access_count": 1
        })

    def retrieve_active(self, current_time=None, threshold=0.3):
        now = current_time or time.time()
        active = []
        for mem in self.memories:
            delta_t = max(0.0, now - mem["created_at"])
            retention = math.exp(-self.decay_rate * delta_t) * mem["importance"] * math.log(1 + mem["access_count"])
            if retention >= threshold:
                active.append((retention, mem["content"]))
        active.sort(key=lambda x: x[0], reverse=True)
        return [{"retention": round(r, 4), "content": c} for r, c in active]
