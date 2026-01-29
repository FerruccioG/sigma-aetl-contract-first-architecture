# 🏛️ Architectural Decision Records (ADR)

This document captures the **key architectural decisions** behind  
**SIGMA-AETL v1.0.0** and the **rationale** for each choice.

🎯 **Purpose**  
Preserve **design intent**, not just implementation details — so future readers understand *why* the system looks the way it does.

---

## 📜 ADR-001: Contract-First Ingestion

### 🧠 Decision  
All data is validated against an **explicit schema contract** at ingestion time.

### ❓ Rationale  
Upstream systems are inherently volatile. Allowing invalid or partially valid data to flow downstream leads to:

- Silent corruption 🕳️
- Compounding operational debt 💸
- Loss of trust in analytics 📉

### ✅ Consequences
- ❌ Invalid data is rejected early
- 📐 Schema drift becomes explicit and visible
- 🔒 Downstream systems can trust ingested data

---

## 🔎 ADR-002: Validator as a Separate Service

### 🧠 Decision  
Schema validation is performed by an **external FastAPI service** using **Pydantic**, not embedded inside the orchestration layer.

### ❓ Rationale
- 🧩 Single source of truth for schema enforcement
- 🧪 Stateless, testable, and reusable
- 📦 Independent versioning and scaling

### ✅ Consequences
- 🧭 Orchestration remains thin and deterministic
- 📋 Validation logic is centralized and auditable

---

## 🔀 ADR-003: Explicit TRUE / FALSE Routing

### 🧠 Decision  
The pipeline branches explicitly into:

- ✅ **TRUE** (valid payloads)
- ❌ **FALSE** (invalid payloads)

Based strictly on the validator response.

### ❓ Rationale  
Implicit failure handling hides problems.  
Failures must be **first-class citizens**, not logs or side effects.

### ✅ Consequences
- 🚫 No silent drops
- 🔍 Failures are queryable and replayable
- 🧠 Clear operational visibility

---

## 🔁 ADR-004: Application-Level Idempotency

### 🧠 Decision  
Idempotency is enforced at the **application layer** using:

- 🆔 Machine-generated identifiers
- 🔐 MongoDB unique indexes

### ❓ Rationale  
Kafka provides **at-least-once delivery**.  
Exactly-once semantics must be enforced explicitly at the storage boundary.

### ✅ Consequences
- 🔄 Safe retries
- ♻️ Safe replays
- 🎯 Deterministic writes

---

## 🗄️ ADR-005: MongoDB as Persistence Layer

### 🧠 Decision  
MongoDB is used for **both validated and failed payload storage**.

### ❓ Rationale
- 🧬 Flexible document storage
- ⚡ Strong indexing capabilities
- 🕵️ Natural fit for audit and metadata-rich records

### ✅ Consequences
- 🔎 Fast lookup by identifiers
- 🧾 Strong replay and forensic analysis capabilities

---

## 🚨 ADR-006: Failure Pipeline as First-Class Citizen

### 🧠 Decision  
Invalid payloads are **normalized, enriched, and persisted** — never discarded.

### ❓ Rationale  
Failures contain valuable signals:
- 📉 Schema mismatches
- 🐞 Producer bugs
- 📜 Contract violations

### ✅ Consequences
- 🧩 Root cause analysis becomes possible
- 🔁 Failures can be replayed after fixes
- 🧠 No loss of diagnostic data

---

## 🤖 ADR-007: Optional AI-Assisted Diagnostics

### 🧠 Decision  
AI diagnostics are **optional, advisory, and non-blocking**.

### ❓ Rationale  
AI should assist humans — **never** affect correctness or execution flow.

### ✅ Consequences
- 🧮 No AI dependency for correctness
- 🧱 Deterministic execution preserved
- 💬 Enhanced failure explainability

---

## 🧊 ADR-008: Frozen Contract Versioning

### 🧠 Decision  
**SIGMA-AETL v1.0.0 is frozen.**  
All changes require a new version.

### ❓ Rationale  
Implicit schema changes break trust, reproducibility, and auditability.

### ✅ Consequences
- 📈 Predictable evolution
- 🧩 Safe coexistence of multiple versions
- 🗺️ Clear migration paths

---

📌 **Summary**  
These decisions collectively ensure that SIGMA-AETL is:

- Deterministic 🧮  
- Replay-safe 🔁  
- Contractually enforced 📜  
- Production-hardened 🛡️  

They are **intentional**, **defensible**, and **non-negotiable** at v1.0.
