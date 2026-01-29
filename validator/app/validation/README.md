✅ Validation Logic — SIGMA-AETL Validator

This folder contains the authoritative validation logic for the SIGMA-AETL ingestion pipeline.

All correctness decisions are made here.

🎯 Responsibility

The validation layer is responsible for:

📜 Enforcing schema contracts (via Pydantic)

🚫 Rejecting invalid payloads deterministically

🟢 Producing explicit PASS / FAIL outcomes

🧾 Generating structured validation errors

🔒 Acting as the single source of truth for ingestion correctness

If validation fails here, the payload does not proceed as valid data.

🧠 Contract-First Enforcement

Validation is performed:

🕰 At ingestion time

📍 Before orchestration branching

🧱 Before persistence

🧪 Before any transformation

There is no downstream “fixing” of bad data.

🔐 Design Guarantees

The validation logic enforces the following guarantees:

🧊 Deterministic — same input, same result

🚫 No heuristics

🚫 No guesses

🚫 No auto-repair

🔁 Replay-safe

🧾 Fully auditable

Every failure is explicit and explainable.

🔁 PASS / FAIL Contract

Validation produces a binary, irreversible outcome:

✅ PASS
Payload conforms exactly to the contract and may proceed.

❌ FAIL
Payload violates one or more contract rules and is rejected.

There is no partial acceptance.

🧬 Relationship to Orchestration

The validator:

🧠 Makes the decision

🚦 Returns PASS or FAIL

🧭 Does not route data

🛠 Does not mutate payloads

Routing is handled by orchestration (n8n), based solely on the validator’s output.

🤖 Relationship to AI Diagnostics

AI diagnostics:

Run after validation

Operate only on FAILED payloads

Are 🧩 advisory only

Have ❌ zero authority

Validation logic is never influenced by AI output.

🧭 Change Policy

⚠️ This validation logic is frozen for v1.0.

Any change to:

Schema shape

Field semantics

Validation rules

Requires:

🆕 A new schema version

🆕 A new validator version

🆕 Explicit orchestration updates

🧾 Summary

This folder is where truth is enforced.

Contracts are upheld

Invalid data is rejected

Correctness is guaranteed

Downstream systems are protected

If validation changes, the contract changes.
