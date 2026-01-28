sigma-aetl-contract-first-architecture

Contract-first, Kafka-driven n8n ETL workflow with explicit Pydantic validation, deterministic failure routing, idempotent persistence, and a private AI diagnostics agent via Ollama, persisting into MongoDB.

Overview

SIGMA-AETL v1.0 is a contract-first, event-driven ingestion architecture designed to harden the ingestion boundary against upstream instability while preserving replayability, auditability, and operational confidence.

Rather than relying on downstream transformations to “fix” data, this system enforces explicit data contracts at ingestion time, routes failures deterministically, and guarantees idempotent persistence under retries and replays.

This repository is published as a reference architecture and educational demo showcasing production-grade ingestion design patterns.

Core Design Goals

Enforce schema correctness at ingestion time, not downstream

Treat invalid data as first-class, not as logs or side effects

Guarantee idempotent, replay-safe persistence

Isolate failures explicitly without contaminating valid datasets

Make AI advisory, private, and non-blocking

Freeze contracts to prevent accidental schema drift

Architecture Summary

SIGMA-AETL is architected as a contract-first ingestion system, not a transformation-centric ETL pipeline.

High-Level Flow

Kafka acts as a durable, decoupled transport layer

Payloads are validated by an external FastAPI + Pydantic validator

The validator returns a deterministic PASSED / FAILED contract response

n8n orchestrates execution with explicit TRUE / FALSE branches

Valid data is persisted into a canonical dataset

Invalid data is normalized, enriched, and persisted into a failure dataset

Failures may optionally be analyzed by a private AI diagnostics agent via Ollama

Kafka provides delivery guarantees — it is not trusted for correctness.

Contract-First Validation

All semantic validation is delegated to a stateless validator service implemented with FastAPI and Pydantic.

The validator is the single source of truth

Validation is side-effect free

Schemas are explicit and immutable per version

Output is deterministic:

PASSED → canonicalized clean data

FAILED → structured validation errors

There is no post-validation mutation or heuristic correction by design.

Explicit Failure Routing

Execution branches explicitly based on validation outcome:

TRUE Path (Validation Passed)

Operates only on schema-validated payloads

Writes canonical data to validated_shipments

Enforces uniqueness via MongoDB indexes

Safe under retries and replays

FALSE Path (Validation Failed)

Treated as a first-class pipeline

Invalid payloads are:

normalized into a failure schema

enriched with ETL, transport, and execution metadata

persisted as immutable failure records

No silent drops, no logs-only failures

Failures are observable, queryable, and replayable.

Idempotency & Replay Safety

Idempotency is enforced at the application layer, not inferred.

Each execution generates a machine-generated identifier

Identifiers are persisted with MongoDB unique indexes

Guarantees exactly-once semantics at the storage boundary

Safe under:

Kafka at-least-once delivery

orchestrator retries

manual replays

Both validated and failed datasets are independently indexed for forensic analysis.

AI-Assisted Diagnostics (Optional)

The failure pipeline optionally integrates a private AI diagnostics subsystem.

Powered by internal language models served via Ollama

Operates on normalized failure records

Produces:

probable root causes

remediation suggestions

business impact hints

Advisory only — non-blocking and side-effect free

AI enhances observability without influencing correctness guarantees.

Versioning & Immutability

The pipeline is frozen at v1.0.

Contracts are immutable

Schema changes require an explicit version bump

Parallel contract versions can coexist safely

Prevents implicit coupling and silent breaking changes

This mirrors production-grade API versioning discipline.

Technology Stack

Kafka — event transport & decoupling

FastAPI + Pydantic — contract enforcement

n8n — orchestration & routing

MongoDB — idempotent persistence & indexing

Ollama — private AI diagnostics agent

What This Repository Is (and Is Not)

+ A reference implementation of a production-grade ingestion architecture
+ A teaching artifact demonstrating contract-first ETL design
+ A reproducible demo showing explicit failure isolation

- Not a turnkey production deployment
- Not a generic ETL template
- Not an AI-driven decision system

License

MIT License — published for knowledge sharing, reproducibility, and architectural clarity.

The goal is not code hoarding, but demonstrating how complex ingestion problems can be made deterministic, observable, and safe.

Author

Designed and implemented by Ferruccio Guicciardi
Contract-first ingestion • Data engineering • Private AI systems