## AI Diagnostics Subsystem

SIGMA-AETL integrates an optional, non-blocking AI diagnostics agent
used exclusively in the FAILED ingestion path.

- Model: qwen2.5:7b
- Runtime: Ollama (local, private, offline-capable)
- Role: Advisory diagnostics only
- Authority: NONE (cannot influence pipeline correctness)

The AI agent analyzes normalized failure records and may suggest:
- Probable root causes
- Field-level validation explanations
- Remediation hints

The agent:
- Is never part of the ingestion decision
- Does not mutate payloads
- Does not block execution
- Can be disabled without affecting correctness

This preserves deterministic, contract-first guarantees.
