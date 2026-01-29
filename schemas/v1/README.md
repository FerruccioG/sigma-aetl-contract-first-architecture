
# 📦 SIGMA-AETL Schema Contracts — v1.0 (Frozen)

🧱 **Versioned, immutable schema definitions for SIGMA-AETL v1.0**

This directory contains the **authoritative schema contracts** used by the SIGMA-AETL validator service to enforce ingestion correctness.

⚠️ **This version (`v1`) is frozen.**  
Any modification requires a **new version directory** (`v2`, `v3`, …).

---

## 🧠 Design Intent

Schemas in this folder define the **hard ingestion boundary** of the pipeline.

They are designed to ensure:

- 🛑 Invalid data never enters downstream systems
- 🔁 Replays and retries are deterministic
- 📜 Validation behavior is predictable and auditable
- 🧩 Schema evolution is explicit, not implicit

These files are not just Python modules —  
they are **formal data contracts**.

---

## 📂 File Overview

### 📄 `base.py`
**Shared schema foundations**

Intended to hold:

- Common Pydantic base classes
- Shared configuration (e.g. strict mode, forbidding extra fields)
- Cross-schema defaults and behaviors

📌 Purpose: enforce **consistent validation semantics** across all schemas.

---

### 📄 `common.py`
**Reusable domain primitives**

Intended to define:

- Common field types (IDs, timestamps, enums)
- Shared validators
- Cross-cutting constraints reused by multiple schemas

📌 Purpose: prevent duplication and ensure **semantic consistency**.

---

### 📄 `shipment.py`
**Primary ingestion contract**

Defines the **canonical payload structure** for shipment ingestion.

Responsibilities include:

- Required business fields
- Strong typing
- Validation constraints
- Explicit optional vs required semantics

📌 This file represents the **single source of truth** for shipment ingestion correctness.

---

### 📄 `README.md`
**Version-level contract documentation**

Explains:

- Why this version exists
- Why it is frozen
- How it should be extended (never modified)

📌 This file is part of the contract itself.

---

## 🔒 Versioning Rules (Strict)

- ✅ `v1` schemas are immutable
- ❌ No backward-incompatible changes allowed
- 🔀 Any evolution requires:
  - New version directory
  - New validator contract
  - Explicit orchestration changes

Multiple schema versions may coexist safely.

---

## 🛡️ Validation Guarantees

Every payload is treated deterministically:

✔️ Valid → canonicalized and accepted  
❌ Invalid → rejected with structured errors  

🚫 Partial acceptance is not allowed  
🚫 Best-effort parsing is intentionally avoided  

---

## 🎯 Why This Matters

By enforcing schema contracts at ingestion time:

- 🧱 Downstream systems are insulated from upstream instability
- 🔁 Reprocessing is safe by design
- 🔍 Data quality issues are visible and auditable
- 🧘 Operational confidence is preserved over time

---

## 📜 Final Reminder

🚨 These schemas are **contracts**, not suggestions.  
🧾 If the data does not match — **it does not enter the system**.
