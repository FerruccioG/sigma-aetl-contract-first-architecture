# n8n Orchestration Layer — SIGMA-AETL v1.0
# n8n workflow definitions and orchestration logic for the SIGMA-AETL pipeline.

This directory contains the **n8n workflow definitions** that orchestrate the SIGMA-AETL v1.0 pipeline.

The orchestration layer is intentionally lightweight and deterministic. It is **not responsible for business logic, schema enforcement, or data correctness**. Its sole role is to coordinate execution based on explicit validation outcomes.

---

## Design Principles

- **Contract-first execution**
  - All payload validation is delegated to an external validator service.
  - n8n does not infer correctness or attempt to repair data.

- **Explicit TRUE / FALSE branching**
  - Workflow execution is deterministically split based on validator response:
    - `TRUE` → validated, schema-compliant data
    - `FALSE` → rejected, invalid data
  - No heuristic or conditional mutation is allowed post-validation.

- **Failure-first architecture**
  - Invalid payloads are treated as first-class records.
  - Failures are normalized, enriched with metadata, and persisted independently.

- **Idempotent by design**
  - Orchestration is safe under retries and replays.
  - Uniqueness and exactly-once semantics are enforced downstream via MongoDB indexes.

---

## Included Workflows

### `sigma-aetl-v1.json`

Production-frozen n8n workflow implementing:

- Kafka-triggered ingestion
- Payload unwrapping and normalization
- External contract validation via HTTP
- Explicit TRUE / FALSE execution paths
- Clean data persistence for validated payloads
- Failure normalization, metadata enrichment, and persistence
- Optional AI-assisted diagnostics on the failure path

This workflow is **version-frozen at v1.0**.  
Any behavioral or contract change requires a new workflow version.

---

## What This Layer Does *Not* Do

- No schema inference
- No data correction or coercion
- No hidden retries with side effects
- No downstream “fix-up” logic

All correctness guarantees are enforced **before** orchestration decisions are made.

---

## Operational Notes

- Kafka provides transport and decoupling only.
- Validator response is the single source of truth.
- n8n branching logic must remain deterministic and side-effect-free.

This orchestration layer is designed to be **observable, replay-safe, and boring** — exactly what you want in production.
