# 🛡️ SIGMA-AETL Validator Service (v1.0 — Frozen)

🚪 **Contract-first ingestion gate for the SIGMA-AETL pipeline**

The SIGMA-AETL Validator is a **standalone, stateless validation service** responsible for enforcing all data contracts **at ingestion time**.

It is the **single source of truth** for determining whether a payload is accepted or rejected by the pipeline.

---

## 🎯 Core Responsibilities

The validator exists to:

- 📜 Enforce schema contracts using **FastAPI + Pydantic**
- 🚫 Reject invalid payloads deterministically
- 🧼 Canonicalize valid payloads into a clean, normalized form
- 🔀 Return an explicit **PASSED / FAILED** contract response
- 🧱 Prevent bad data from entering downstream systems

This service does **not** orchestrate, transform, enrich, or store data.

---

## 🧠 Architectural Position
```bash
Kafka Event
↓
Validator Service (FastAPI + Pydantic)
↓
Contract Response
├─ PASSED → TRUE branch
└─ FAILED → FALSE branch
```

📌 The validator runs **before** any business processing.

---

## 🧩 Design Principles

### 🔒 Contract-First
- Schemas are authoritative
- Validation is deterministic
- No heuristic correction
- No best-effort parsing

### 🧪 Pure & Stateless
- No database writes
- No side effects
- Same input → same output

### 🧭 Single Authority
- Validator decisions are final
- Orchestration must obey the response
- No downstream override allowed

---

## 🧾 Validation Output Contract

The validator always returns a **machine-readable contract**:

### ✅ PASSED
- Canonicalized payload
- Normalized field formats
- Guaranteed schema compliance

### ❌ FAILED
- Structured validation errors
- Explicit failure reasons
- No partial acceptance

📌 The validator never throws business exceptions downstream.

---

## ⚙️ Implementation Stack

- 🐍 **FastAPI** — API boundary
- 📐 **Pydantic** — schema enforcement
- 🧪 **Strict validation mode**
- 📦 **Dockerized** for reproducibility
- 🧠 **Versioned contracts** (v1 frozen)

---

## 🚫 What This Service Does NOT Do

- ❌ Does not store data
- ❌ Does not mutate payloads post-validation
- ❌ Does not retry or reprocess
- ❌ Does not call AI
- ❌ Does not contain business logic

Those responsibilities belong elsewhere by design.

---

## 🔐 Versioning Rules

- 🔒 Validator v1.0 is **frozen**
- ❌ No schema changes allowed in-place
- 🔁 Any evolution requires:
  - New schema version
  - New validator contract
  - New orchestration wiring

Multiple validator versions may coexist safely.

---

## 🧘 Why This Matters

By isolating validation into a dedicated service:

- 🔍 Failures are explicit and inspectable
- 🔁 Replays are safe and deterministic
- 🧱 Downstream systems are protected
- 🧠 Complexity is contained at the boundary

---

## 📜 Final Note

🚨 **This validator is not a helper — it is a gatekeeper.**

If the payload does not conform to the contract:  
**It does not enter the system.**
