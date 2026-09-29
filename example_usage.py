from client import TemporalDecayMemory

mem = TemporalDecayMemory(decay_rate=0.05)
mem.store("Important project milestone deadline", importance=3.0)
mem.store("Casual greeting from guest", importance=0.5)

active_items = mem.retrieve_active(threshold=0.5)
print("Active Retained Memories:", active_items)
