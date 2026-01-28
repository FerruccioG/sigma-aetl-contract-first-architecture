# Schema Contracts — SIGMA-AETL v1.0
# Pydantic schemas and data contracts used to enforce validation boundaries.

This directory contains the **immutable data contracts** for SIGMA-AETL v1.0.

Schemas in this folder define the **ingestion boundary** for the system. Any payload entering the pipeline must conform to these contracts or be explicitly rejected.

---

## Contract-First Philosophy

SIGMA-AETL enforces correctness at **ingestion time**, not downstream.

- Schemas are authoritative
- Validation is deterministic
- Invalid data is rejected, not repaired
- Schema drift is treated as a breaking change

These schemas are implemented and enforced using **Pydantic** in the validator service.

---

## Versioning Rules

- `v1` schemas are **frozen**
- No backward-incompatible changes are allowed
- Any schema evolution requires:
  - A new version directory (`v2`, `v3`, …)
  - A new validator contract
  - Explicit orchestration changes

Multiple schema versions may coexist safely.

---

## Included Schemas

### `shipment.py`

Defines the canonical payload structure for shipment ingestion, including:

- Required business fields
- Strongly typed attributes
- Validation constraints
- Explicit optional vs required semantics

This schema is the **single source of truth** for ingestion correctness.

---

## Validation Guarantees

- Payloads are either:
  - **Accepted** and canonicalized
  - **Rejected** with structured validation errors
- Partial acceptance is not allowed
- Best-effort parsing is intentionally avoided

---

## Why This Matters

By freezing schema contracts and enforcing them at the boundary:

- Downstream systems are protected from upstream instability
- Replay and reprocessing are safe
- Data quality issues are isolated and auditable
- Operational confidence is preserved as systems evolve

These schemas are **not suggestions** — they are contracts.
