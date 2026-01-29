# 🧠 n8n Workflow — SIGMA-AETL v1.0 (Contract-Frozen)

This directory contains the **n8n workflow implementation** for **SIGMA-AETL v1.0**.

⚠️ **IMPORTANT — VERSION FREEZE NOTICE**

> 🧊 **This workflow is frozen at v1.0 and must NOT be edited in place.**  
> Any schema, contract, routing, or behavioral change **requires a new, explicitly versioned workflow** (e.g. `v1.1`, `v2.0`).

This is a **deliberate architectural decision** to preserve:
- Determinism
- Replay safety
- Auditability
- Contract integrity

---

## 🎯 Purpose of This Workflow

This n8n workflow acts as the **orchestration layer only**.

It is responsible for:
- 📨 Receiving Kafka-triggered ingestion events
- 🔗 Calling the external validator service
- 🔀 Branching execution **explicitly** into TRUE / FALSE paths
- 📦 Persisting results into MongoDB

It does **not**:
- ❌ Validate schemas
- ❌ Infer correctness
- ❌ Mutate payloads
- ❌ Repair bad data

All correctness decisions are delegated to the **SIGMA-AETL Validator**.

---

## 🔀 Execution Flow (High-Level)

1. 📥 **Kafka Event Trigger**
2. 🧪 **Validator Call (FastAPI + Pydantic)**
3. 🟢 **TRUE Path**
   - Clean, schema-valid payload
   - Insert into `validated_shipments`
4. 🔴 **FALSE Path**
   - Normalized failure record
   - Enriched with ETL metadata
   - Insert into `failed_shipments`
   - Optional AI diagnostics (non-blocking)

---

## 🧠 Optional AI Diagnostics (FALSE Path Only)

The FALSE branch may optionally invoke a **private, local AI diagnostics agent**.

### 🔧 Requirements
```bash
ollama pull qwen2.5:7b
```
🧩 Characteristics

🧠 Model: qwen2.5:7b

🏠 Runtime: Ollama (local, private, offline-capable)

🧭 Role: Advisory diagnostics only

🚫 Authority: NONE (cannot influence pipeline correctness)

The AI agent:

Suggests probable root causes

Explains validation failures

Proposes remediation hints

The AI agent:

❌ Never affects routing

❌ Never mutates data

❌ Never blocks execution

❌ Can be disabled without impact

This preserves deterministic, contract-first guarantees.

♻️ Idempotency & Replay Safety

This workflow is safe under:

Retries

Replays

Duplicate Kafka delivery

Manual re-execution

Exactly-once behavior is enforced downstream using:

Machine-generated identifiers

MongoDB unique indexes

n8n remains stateless and deterministic by design.

🧊 Versioning Rules (Non-Negotiable)

🧾 Schemas are immutable per version

🔁 No in-place workflow edits

🆕 Any change → new workflow version

📦 Old versions remain deployable and replayable

This prevents silent breakage and schema drift.

🧠 Mental Model

“n8n orchestrates.
The validator decides.
MongoDB enforces.
AI advises — but never commands.”

If this workflow feels boring, it’s working as intended.
