# SIGMA-AETL Roadmap

This roadmap describes the intentional evolution of the SIGMA-AETL
contract-first ingestion architecture beyond the frozen v1.0.0 release.

The roadmap is **directional**, not a commitment to implementation.
All future changes must preserve the core principles established in v1.0.0:
contract immutability, explicit validation, deterministic routing, and
idempotent persistence.

---

## v1.0.0 — Contract Frozen (Released)

Status: ✅ Released

- Contract-first ingestion boundary
- Kafka-driven event transport
- FastAPI + Pydantic validator enforcing schema contracts
- Explicit TRUE / FALSE routing paths
- Idempotent persistence via machine-generated identifiers
- MongoDB unique indexing for replay safety
- First-class failure isolation and auditability
- Optional private AI-assisted diagnostics via Ollama

This version is **immutable**.

---

## v1.1.0 — Multi-Contract Support (Planned)

Status: 🧭 Planned

Goals:
- Support multiple schema versions in parallel
- Allow controlled coexistence of v1 and v2 contracts
- Enable phased upstream migrations

Potential Enhancements:
- Schema registry abstraction (filesystem or service-based)
- Version-aware validator routing
- Contract negotiation metadata

---

## v1.2.0 — Observability & Metrics (Planned)

Status: 🧭 Planned

Goals:
- Improve operational visibility
- Enable SLO/SLA-style monitoring

Potential Enhancements:
- Validation latency metrics
- Failure rate dashboards
- Replay volume tracking
- Structured logs for validator and orchestration layers

---

## v2.0.0 — Distributed Validator & Scaling (Exploratory)

Status: 🧪 Exploratory

Goals:
- Horizontal validator scaling
- Stateless validator pools
- Increased throughput without sacrificing correctness

Potential Enhancements:
- Validator sharding
- Dedicated validation queues
- Backpressure-aware orchestration

---

## Non-Goals

The following are explicitly **out of scope** for SIGMA-AETL:

- Silent schema evolution
- Heuristic auto-correction of invalid payloads
- Implicit retries without idempotency guarantees
- Ingestion without contract validation

SIGMA-AETL prioritizes **correctness, traceability, and safety** over raw throughput.
