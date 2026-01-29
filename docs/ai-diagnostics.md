🧠 AI Diagnostics Subsystem

SIGMA-AETL integrates an optional, non-blocking AI diagnostics agent 🧩
This component is used exclusively in the FAILED ingestion path ❌ and is deliberately isolated from the core validation logic.

🔍 Purpose & Scope

The AI diagnostics subsystem exists to explain failures, not to fix them.

It provides advisory insights only and never participates in ingestion decisions ⚖️
This preserves SIGMA-AETL’s deterministic, contract-first guarantees 🧱

⚙️ Technical Characteristics

🧠 Model: qwen2.5:7b

🏃 Runtime: Ollama (local, private, offline-capable)

🎯 Role: Advisory diagnostics only

🚫 Authority: NONE — cannot influence pipeline correctness

🧪 What the AI Analyzes

The agent operates on normalized failure records 📄 produced by the FALSE path.

It may suggest:

🔎 Probable root causes

🧩 Field-level validation explanations

🛠️ Remediation hints for upstream producers

These outputs are annotations, not actions.

🚧 Explicit Non-Goals (By Design)

The AI agent:

🚫 Is never part of the ingestion decision

🚫 Does not mutate payloads

🚫 Does not block execution

🚫 Does not override schema enforcement

🔌 Can be disabled entirely without affecting correctness

This ensures that:

Validation remains deterministic, auditable, and reproducible — with or without AI.

🧱 Architectural Rationale

AI is intentionally placed after validation, not during it.

This avoids:

❌ Non-deterministic ingestion

❌ Heuristic data acceptance

❌ Hidden coupling between AI and data correctness

❌ “Smart” pipelines that cannot be trusted under replay

SIGMA-AETL treats AI as observability, not authority 👁️‍🗨️

📦 Model Distribution Policy

🚫 Model binaries are intentionally NOT committed to this repository.

This repository documents:

🔌 Integration patterns

📐 Architectural boundaries

🧭 Operational intent

Not:

🧠 Model weights

📦 Runtime artifacts

🔒 Vendor-specific binaries

This keeps the project:

✅ Lightweight

✅ Reproducible

✅ License-clean

✅ Security-aware


📈 FALSE Path — Diagnostic Flow (Mermaid Sequence Diagram)
sequenceDiagram
    participant Kafka as Kafka Event Trigger
    participant n8n as n8n Orchestrator
    participant Validator as SIGMA-AETL Validator (FastAPI + Pydantic)
    participant MongoFail as MongoDB (failed_shipments)
    participant AI as AI Diagnostics (Ollama)

    Kafka->>n8n: Event received
    n8n->>Validator: POST /api/validate
    Validator-->>n8n: FAILED + structured errors
    n8n->>MongoFail: Persist normalized failure record
    n8n->>AI: Submit failure context (optional)
    AI-->>n8n: Advisory diagnostics (non-blocking)

🧠 Key Properties

❌ Validation always happens before AI

🧱 Failure records are persisted first

🔌 AI enrichment is optional and asynchronous

🔁 Replays produce identical validation outcomes

🚫 Why AI Is Explicitly Excluded from the TRUE Path

AI is deliberately forbidden from participating in the TRUE (validated) ingestion path.

❗ Design Reasons

🧮 Determinism:
AI introduces probabilistic behavior — unacceptable for data correctness.

🔁 Replay Safety:
Re-running historical data must produce identical results.

📜 Auditability:
Schema validation produces explainable, reproducible outcomes.

🔒 Trust Boundary:
AI is not a source of truth.

🧱 Architectural Rule

If data passes validation, AI has nothing to say.

The TRUE path operates on:

✅ Canonicalized payloads

✅ Versioned schema contracts

✅ Deterministic logic only

No heuristics. No guesses. No exceptions.

🧪 Sample AI Diagnostic Output (Non-Authoritative)

⚠️ Important:
The following output is illustrative only.
AI diagnostics do not influence pipeline execution.

```json
{
  "diagnostic_summary": "Payload failed schema validation due to negative numeric value and missing required field.",
  "probable_root_cause": "Upstream producer emitting partial payload during retry sequence.",
  "field_analysis": {
    "weight_kg": "Value must be greater than zero as per contract.",
    "priority": "Required field missing."
  },
  "recommended_actions": [
    "Validate payload construction before Kafka publish.",
    "Ensure retry logic does not drop required fields."
  ],
  "confidence_level": "medium"
}
```

🧠 Interpretation Rules

📝 Advisory only

🚫 Cannot override validator

🚫 Cannot mutate stored records

📎 Stored as metadata, not truth
