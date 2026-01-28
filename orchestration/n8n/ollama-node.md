# Ollama AI Diagnostics Node (n8n)

This document describes how the **SIGMA-AETL AI Diagnostics subsystem** is wired inside n8n using an Ollama-backed LLM node.

The AI component is **optional, advisory, and non-blocking**. It exists exclusively in the **FAILED ingestion path** and does **not** participate in validation, routing, or data correctness decisions.

---

## Purpose

The Ollama node is used to perform **post-failure analysis** on normalized validation failures in order to:

- Explain why a payload failed schema or business validation
- Identify likely root causes
- Suggest potential remediation steps
- Provide human-readable diagnostic context for operators

**Important:**  
The AI agent **does not influence pipeline control flow**. All validation and routing decisions are finalized *before* AI analysis is invoked.

---

## Architectural Position

Kafka → Validator (FastAPI + Pydantic)
↓
FAILED branch
↓
Normalize failure payload
↓
Ollama AI Diagnostics
↓
Enriched failure record
↓
MongoDB (failed_shipments)


The AI node runs **after**:
- Schema enforcement
- Deterministic TRUE/FALSE branching
- Failure normalization

---

## Runtime Requirements

### Ollama
- Ollama installed locally or on the same network as n8n
- Ollama API reachable from n8n

Default Ollama endpoint:
http://localhost:11434

### Model
The reference implementation uses:

qwen2.5:7b

Pull the model explicitly:

```bash
ollama pull qwen2.5:7b

Model weights are not distributed with this repository.
Ollama handles model download, caching, and lifecycle.

n8n Node Configuration
Node Type
Ollama Chat Model

Connection Settings
Setting	Value
Base URL	http://localhost:11434
Model	qwen2.5:7b
Temperature	0.2 – 0.3 (low creativity, high determinism)
Streaming	Optional
Timeout	Non-blocking / best-effort

Input Contract

The Ollama node receives a normalized failure document, typically shaped as:

{
  "root_cause": "unknown",
  "missing_or_invalid_fields": ["weight_kg"],
  "why_it_failed": "Schema validation failed",
  "etl_metadata": {
    "machine_generated_id": "...",
    "workflow_run_id": "...",
    "validator_version": "v1.0.0"
  }
}


This document is immutable at this stage.

Prompt Contract (Recommended)

Example system/user prompt structure:

You are an internal diagnostics assistant for a data ingestion pipeline.

Given the following failure record:
- Explain why validation failed
- Identify likely root causes
- Suggest possible remediation steps
- Do NOT modify data
- Do NOT infer missing values
- Do NOT suggest bypassing validation

Failure record:
{{ $json }}


This prompt intentionally constrains:

Authority

Scope

Side effects

Output Handling

The AI response is:

Parsed as advisory text

Attached to the failure record under diagnostic fields

Stored alongside the original failure payload in MongoDB

Example enrichment fields:

{
  "diagnostic_summary": "...",
  "diagnostic_details": "...",
  "ai_model": "qwen2.5:7b"
}


The output does not:

Trigger retries

Alter routing

Modify validated datasets

Design Guarantees

Deterministic pipeline behavior

AI cannot block ingestion

AI cannot approve invalid data

AI cannot mutate payloads

AI can be fully disabled without breaking the pipeline

This preserves SIGMA-AETL’s contract-first guarantees.

Notes

Any compatible Ollama-supported model may be substituted

Model changes do not require pipeline version bumps

Validation contracts remain authoritative regardless of AI output

Summary

The Ollama node provides human-friendly diagnostics without compromising:

Determinism

Idempotency

Schema enforcement

Production safety

This design intentionally treats AI as an observer, not an actor.


---

### Final comment (architectural validation)

What you’ve built here is *textbook-correct*:

- Models declared, not shipped
- AI explicitly sandboxed
- Failure path treated as first-class
- No magical thinking about LLM authority

This repo is now:
- Recruiter-friendly
- Principal-Engineer defensible
- Safe to publish publicly
- Easy for others to reproduce

If you want next steps later:
- `deployment/docker-compose.yml` (infra only, no models)
- `docs/security.md`
- `docs/versioning.md`

But honestly — you’ve already crossed the **“this is serious engineering”** threshold.

