# 🧠 Ollama AI Diagnostics Node (n8n)

This document describes how the **SIGMA-AETL AI Diagnostics subsystem** is wired inside **n8n** using a **private, Ollama-backed LLM**.

⚠️ **Important upfront:**  
The AI component is **optional**, **advisory**, and **non-blocking**.  
It exists **exclusively in the FAILED ingestion path** and **does not participate** in validation, routing, or data correctness decisions.

---

## 🎯 Purpose

The Ollama AI node is used for **post-failure diagnostics only**, operating on **already-rejected payloads**.

Its role is to:
- 🧩 Explain *why* a payload failed schema or contract validation
- 🔍 Identify likely root causes
- 🛠️ Suggest potential remediation steps
- 🧠 Provide human-readable diagnostic context for operators

🚫 **What it never does**
- Influence pipeline control flow
- Approve or reject data
- Modify payloads
- Bypass validation rules

All validation and routing decisions are **finalized before** the AI node is invoked.

---

## 🧱 Architectural Position

Kafka Event Trigger
↓
Validator (FastAPI + Pydantic)
↓
Deterministic TRUE / FALSE Branch
↓
FAILED Path Only
↓
Failure Normalization
↓
🧠 Ollama AI Diagnostics (Advisory)
↓
Enriched Failure Record
↓
MongoDB (failed_shipments)
```yaml

The AI node runs **only after**:
- ✅ Schema enforcement
- ✅ Deterministic TRUE/FALSE branching
- ✅ Failure normalization

---

## 🧠 Design Philosophy

> **AI is an observer, not an actor.**

The pipeline is correct *without* AI.  
AI exists to **explain**, not to **decide**.

This preserves:
- Determinism
- Idempotency
- Contract-first guarantees
- Production safety

---

## ⚙️ Runtime Requirements

### 🏠 Ollama Runtime
- Ollama installed locally or reachable from n8n
- Ollama API accessible from n8n

**Default endpoint**
```
http://localhost:11434
```yaml

---

## 🧠 Model Configuration

The reference implementation uses:

- **Model:** `qwen2.5:7b`

Pull explicitly:
```bash
ollama pull qwen2.5:7b
```
📦 Important

Model weights are not committed to this repository

Ollama handles model download, caching, and lifecycle

This repo documents integration patterns, not binaries

🔌 n8n Node Configuration
Node Type

Ollama Chat Model

Connection Settings

| Setting     | Value                                     |
| ----------- | ----------------------------------------- |
| Base URL    | `http://localhost:11434`                  |
| Model       | `qwen2.5:7b`                              |
| Temperature | `0.2 – 0.3` (low creativity, high signal) |
| Streaming   | Optional                                  |
| Timeout     | Best-effort / non-blocking                |

📥 Input Contract

The Ollama node receives a normalized failure document, typically shaped as:
```json
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
```
🔒 This document is immutable at this stage.

🧾 Prompt Contract (Recommended)

Example system/user prompt structure:
```text
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
```
This prompt intentionally constrains:

Authority

Scope

Side effects

📤 Output Handling

The AI response is:

Parsed as advisory text

Attached to the failure record

Persisted alongside the original payload in MongoDB

Example enrichment fields:
```json
{
  "diagnostic_summary": "...",
  "diagnostic_details": "...",
  "ai_model": "qwen2.5:7b"
}
```
🚫 The output does not:

Trigger retries

Alter routing

Modify validated datasets

🛡️ Design Guarantees

This design guarantees:

🔁 Deterministic pipeline behavior

🧱 AI cannot block ingestion

🚫 AI cannot approve invalid data

🔒 AI cannot mutate payloads

🔌 AI can be disabled with zero impact

All contract-first guarantees remain intact.

🔄 Model Flexibility

Any Ollama-supported model may be substituted

Model changes do not require pipeline version bumps

Validation contracts remain authoritative regardless of AI output

📌 Summary

The Ollama AI Diagnostics node provides human-friendly insight without compromising:

Determinism

Idempotency

Schema enforcement

Production safety

This is AI done responsibly: sandboxed, advisory, and humble.


