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
