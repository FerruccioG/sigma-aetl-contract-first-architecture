📦 Data Models — SIGMA-AETL Validator

This folder contains internal data models used by the SIGMA-AETL Validator service.

These models support validation, normalization, and diagnostics, but do not define the ingestion contract itself.

🎯 Purpose

Models in this folder are used to:

🧩 Represent internal data structures

🧠 Shape diagnostic and metadata payloads

🧾 Normalize validation error output

🛠 Support internal processing logic

They exist inside the validator boundary.

🧱 Important Distinction

⚠️ These are NOT ingestion contracts.

❌ They are not authoritative

❌ They do not define schema truth

❌ They are not exposed to upstream producers

✅ The authoritative ingestion contract lives in:
```bash
/schemas/v1/
```
Those schemas are enforced via Pydantic at runtime and are immutable for v1.0.

🔐 Design Rules

Models in this folder must follow these rules:

🧊 Deterministic behavior only

🚫 No business logic side effects

🧪 Safe for retries and replays

🔒 Cannot override validation outcomes

They support the contract — they never redefine it.

🧠 Relationship to Diagnostics

Some models may be used to:

Structure AI diagnostic inputs

Normalize failure explanations

Attach advisory metadata to failed records

📌 Even when used by AI diagnostics:

Authority remains zero

Output remains advisory

Validation decisions remain final

🧭 Philosophy

Contracts define truth.
Models support execution.

This separation preserves clarity, safety, and evolvability.

✅ Summary

This folder contains supporting models, not contracts.

It exists to keep the validator:

Clean

Explicit

Deterministic

Easy to evolve without breaking ingestion guarantees
