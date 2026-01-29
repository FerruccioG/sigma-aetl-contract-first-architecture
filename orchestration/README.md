# 🧭 n8n Orchestration Layer — SIGMA-AETL v1.0

**n8n workflow definitions and orchestration logic for the SIGMA-AETL contract-first pipeline.**

This directory contains the **n8n orchestration layer** responsible for coordinating execution flow in **SIGMA-AETL v1.0**.

⚠️ **Important:**  
The orchestration layer is intentionally **lightweight, deterministic, and non-authoritative**.  
It does **not** perform validation, business logic, or data correction.

Its sole responsibility is to **route execution based on explicit validation outcomes**.

---

## 🎯 Design Principles

### 📜 Contract-First Execution
- All payload validation is delegated to an **external validator service**.
- Validation is enforced **before** any orchestration decision.
- n8n **never infers correctness** and **never attempts to repair data**.

---

### 🔀 Explicit TRUE / FALSE Branching
- Workflow execution is deterministically split based on validator response:
  - ✅ **TRUE path** → validated, schema-compliant payloads
  - ❌ **FALSE path** → rejected, invalid payloads
- No heuristics, no soft conditions, no post-validation mutation.

---

### 🚨 Failure-First Architecture
- Invalid payloads are treated as **first-class data**, not logs.
- Failures are:
  - Normalized
  - Enriched with ETL and execution metadata
  - Persisted independently for audit, replay, and diagnostics

---

### ♻️ Idempotent by Design
- Orchestration is **safe under retries and replays**.
- Exactly-once semantics are enforced **downstream** using:
  - Machine-generated identifiers
  - MongoDB unique indexes
- n8n itself remains stateless and deterministic.

---

## 📦 Included Workflows

### 📄 `sigma-aetl-v1.json`

🚀 **Production-frozen n8n workflow implementing:**

- Kafka event-driven ingestion trigger
- Payload unwrapping and normalization
- External contract validation via HTTP (FastAPI + Pydantic)
- Deterministic TRUE / FALSE execution paths
- Clean data persistence for validated payloads
- Failure normalization and metadata enrichment
- Optional AI-assisted diagnostics on the FALSE path (via Ollama)

🔒 This workflow is **version-frozen at v1.0**.  
Any behavioral, structural, or contract change requires an **explicit version bump**.

---

## 🚫 What This Layer Does *Not* Do

- ❌ No schema inference  
- ❌ No data correction or coercion  
- ❌ No hidden retries with side effects  
- ❌ No downstream “fix-up” logic  

All correctness guarantees are enforced **before orchestration begins**.

---

## ⚙️ Operational Notes

- 📦 **Kafka** provides transport and decoupling only — not truth
- ✅ **Validator response** is the single source of truth
- 🧠 **n8n branching logic must remain deterministic and side-effect-free**

This orchestration layer is designed to be:

✨ **Observable**  
♻️ **Replay-safe**  
😌 **Boring by design** — exactly what you want in production

---

> _“If orchestration is exciting, something is wrong.”_
