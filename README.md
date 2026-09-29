# genpark-episodic-memory-temporal-decay-manager-skill

Agent Skill implementing **Ebbinghaus Forgetting Curves & Temporal Memory Consolidation** in 100% Python standard library.

## Architectural Flow
```mermaid
flowchart TD
    Memory["Stored Memory Trace"] --> Curve["Ebbinghaus Retention: R = exp(-lambda * delta_t) * I * log(1 + N)"]
    Clock["Time Elapsed (delta_t)"] --> Curve
    Access["Access Frequency (N)"] --> Curve
    Importance["Initial Importance (I)"] --> Curve
    Curve --> Threshold{"Retention >= Threshold?"}
    Threshold -->|Yes| Retain["Active Episodic Memory Pool"]
    Threshold -->|No| Pruned["Consolidated / Pruned to Inactive"]
```
