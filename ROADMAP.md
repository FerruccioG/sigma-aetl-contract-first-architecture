# SIGMA-AETL Roadmap

This document outlines the **intentional evolution path** of the SIGMA-AETL architecture.

The roadmap reflects a **contract-first, ingestion-boundary–driven philosophy**, prioritizing correctness, determinism, and operational safety over feature velocity.

---

## v1.0.0 — Contract Frozen ✅ (Current)

**Status:** Released  
**Tag:** `v1.0.0-contract-frozen`

The v1.0 release represents a **fully functional, production-grade reference architecture** demonstrating contract-first ingestion and explicit failure isolation.

### Capabilities
- Contract-first ingestion using FastAPI + Pydantic
- Kafka-triggered, event-driven orchestration via n8n
- Explicit TRUE / FALSE execution paths
- Deterministic idempotency using machine-generated identifiers
- Production-grade MongoDB indexing for exactly-once behavior at the application boundary
- First-class failure persistence with structured metadata
- Optional, **non-blocking private AI-assisted diagnostics via Ollama (advisory only, no authority)**

### Guarantees
- Deterministic validation decisions
- Replay-safe ingestion
- Immutable schema contracts
- Auditable failure records
- No implicit data mutation or repair

The v1.0 contract is **frozen**.  
No backward-incompatible changes are permitted.

---

## v1.1.0 — Multi-Contract Support (Planned)

**Goal:** Support parallel schema evolution without breaking existing pipelines.

### Planned Enhancements
- Side-by-side schema versioning (v1, v2, …)
- Multiple validator contracts operating concurrently
- Explicit orchestration routing by schema version
- Safe coexistence of historical and future payload formats
- Preserve strict ingestion-boundary enforcement per contract version

### Non-Goals
- In-place schema mutation
- Implicit backward compatibility
- Silent schema drift handling

---

## v1.2.0 — Observability & Diagnostics Expansion (Optional)

**Goal:** Improve operator insight without compromising determinism.

### Potential Enhancements
- Failure classification metrics (by `root_cause`, field, schema version)
- Aggregated failure trend analysis
- Enriched operational dashboards based on persisted failure data
- Read-only diagnostics views for support and audit use cases

### Explicit Constraints
- No AI-driven acceptance decisions
- No automated payload correction
- No runtime dependency on AI availability

---

## v2.0.0 — Architecture Evolution (Future / Exploratory)

**Goal:** Explore architectural extensions without violating core principles.

### Possible Directions
- Pluggable validator backends
- Alternative orchestration engines
- Cloud-native deployments
- Advanced schema governance tooling

### Hard Constraints (Non-Negotiable)
- Contract-first ingestion remains authoritative
- Validation decisions remain deterministic
- Failures remain first-class data
- Replay safety is preserved
- No hidden or implicit data transformations

---

## Explicit Non-Goals (All Versions)

SIGMA-AETL intentionally does **not** aim to be:
- A self-healing data platform
- An AI-driven ingestion decision engine
- A best-effort parser
- A transformation-heavy ETL framework
- A replacement for downstream analytics or processing engines

---

## Guiding Principle

> **Correctness at ingestion is cheaper than correction downstream.**

The roadmap prioritizes **predictability, auditability, and operational confidence** over convenience or automation.

Changes happen through **versioned contracts**, not silent evolution.

---
