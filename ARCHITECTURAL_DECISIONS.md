# Architectural Decision Records (ADR)

This document captures the key architectural decisions behind
SIGMA-AETL v1.0.0 and the rationale for each choice.

The goal is to preserve **design intent**, not just implementation detail.

---

## ADR-001: Contract-First Ingestion

**Decision**  
All data is validated against an explicit schema contract at ingestion time.

**Rationale**  
Upstream systems are volatile. Allowing invalid or partially valid data
into downstream systems creates silent data corruption and operational debt.

**Consequences**
- Invalid data is rejected early
- Schema drift becomes explicit
- Downstream systems trust ingested data

---

## ADR-002: Validator as a Separate Service

**Decision**  
Schema validation is performed by an external FastAPI service using Pydantic,
not embedded inside the orchestration layer.

**Rationale**
- Single source of truth for schema enforcement
- Stateless, testable, and reusable
- Independent versioning and scaling

**Consequences**
- Orchestration remains thin and deterministic
- Validation logic is centralized and auditable

---

## ADR-003: Explicit TRUE / FALSE Routing

**Decision**  
The pipeline branches explicitly into TRUE (valid) and FALSE (invalid) paths
based on the validator response.

**Rationale**
Implicit failure handling hides problems.
Failures are first-class citizens and must be observable.

**Consequences**
- No silent drops
- Failures are queryable and replayable
- Operational clarity

---

## ADR-004: Application-Level Idempotency

**Decision**  
Idempotency is enforced at the application layer using
machine-generated identifiers and MongoDB unique indexes.

**Rationale**
Kafka provides at-least-once delivery.
Exactly-once semantics must be enforced explicitly at storage boundaries.

**Consequences**
- Safe retries
- Safe replays
- Deterministic writes

---

## ADR-005: MongoDB as Persistence Layer

**Decision**  
MongoDB is used for both validated and failed payload storage.

**Rationale**
- Flexible schema storage
- Strong indexing capabilities
- Natural fit for audit records and metadata-rich documents

**Consequences**
- Fast lookup by identifiers
- Strong replay and forensic capabilities

---

## ADR-006: Failure Pipeline as First-Class Citizen

**Decision**  
Invalid payloads are normalized, enriched, and persisted rather than discarded.

**Rationale**
Failures contain valuable information:
schema mismatches, producer bugs, contract violations.

**Consequences**
- Root cause analysis becomes possible
- Failures can be replayed after fixes
- No loss of diagnostic data

---

## ADR-007: Optional AI-Assisted Diagnostics

**Decision**  
AI diagnostics are advisory, optional, and non-blocking.

**Rationale**
AI should assist humans, not affect correctness or execution flow.

**Consequences**
- No AI dependency for correctness
- Deterministic execution preserved
- Enhanced failure explainability

---

## ADR-008: Frozen Contract Versioning

**Decision**  
v1.0.0 is frozen. All changes require a new version.

**Rationale**
Implicit schema changes break trust and reproducibility.

**Consequences**
- Predictable evolution
- Safe coexistence of versions
- Clear migration paths
