# 📐 Architecture Diagram Legend — SIGMA-AETL

This legend explains the symbols, arrows, and boundaries used in the SIGMA-AETL architecture diagrams.

The goal is to make **authority, responsibility, and data flow unambiguous**.

---

## 🚚 Kafka — Event Transport Only

Kafka is used strictly as:

- 📬 Event delivery
- 🔄 Decoupling
- 🧵 Ordering
- 📈 Backpressure handling

Kafka is **not trusted for correctness**.

❌ No validation  
❌ No schema enforcement  
❌ No business logic  

---

## 🛡️ Validator — Single Source of Truth

The FastAPI + Pydantic validator represents the **ingestion authority boundary**.

Responsibilities:

- 📜 Schema enforcement
- 🧪 Deterministic validation
- 🧭 TRUE / FALSE decision
- 🔒 Contract enforcement

📌 All routing decisions are finalized here.

---

## ✅ TRUE Path — Accepted Data

Represents payloads that:

- ✔ Passed schema validation
- ✔ Were canonicalized
- ✔ Are safe for downstream use

TRUE path guarantees:

- 🧾 Contract compliance
- 🔁 Safe reprocessing
- 📦 Idempotent storage

---

## ❌ FALSE Path — Rejected Data (First-Class)

Represents payloads that:

- ❌ Failed validation
- ❌ Violated schema or constraints

FALSE path is **intentional and first-class**:

- 🧱 Failures are normalized
- 🗂️ Persisted and indexed
- 🔍 Auditable and replayable

FALSE ≠ logs  
FALSE = structured failure data

---

## 🧠 AI Diagnostics — Advisory Boundary

The AI diagnostics subsystem:

- 🧠 Reads failure records
- 📝 Produces explanations
- 💡 Suggests remediation

It has **NO authority**.

❌ Cannot approve data  
❌ Cannot block ingestion  
❌ Cannot mutate payloads  

AI is an **observer, not an actor**.

---

## 🗄️ MongoDB — Application Boundary Guarantees

MongoDB provides:

- 🔑 Unique indexes
- 🔁 Idempotency enforcement
- 🧾 Deterministic persistence

Exactly-once semantics are enforced at the **application boundary**, not the broker.

---

## 🔚 Summary

This architecture enforces:

- 🧊 Contract-first ingestion
- 🛡️ Deterministic validation
- 🔁 Safe replays
- ❌ No hidden logic
- 🧠 AI without authority

**Correctness is explicit. Nothing is implicit.**
