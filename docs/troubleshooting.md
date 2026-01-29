
# 🛠️ Troubleshooting — SIGMA-AETL

This document covers **common issues**, **failure modes**, and **diagnostic steps** when running or experimenting with the SIGMA-AETL contract-first architecture.

The system is intentionally strict. Most “problems” are actually **signals that the architecture is working as designed**.

---

## 🚨 Workflow Executes but Routes to FALSE Branch

### ✅ This is NOT an error
If the workflow completes successfully but follows the **FALSE path**, it means:

- ❌ The payload **did not satisfy the Pydantic schema**
- ❌ One or more required fields were missing or invalid
- ❌ Validation rules were intentionally enforced

### 🔍 What to check
- Validator response payload (`status = FAILED`)
- `errors` array returned by the validator
- Inserted document in `failed_shipments`

📌 **Remember:** FALSE ≠ logs. FALSE = structured, persisted failure data.

---

## 🔌 n8n Cannot Reach Validator

### Symptoms
- HTTP node fails
- Connection refused
- Timeout errors

### Checks
- 🐳 Is the validator container running?
```bash
  docker ps | grep sigma-aetl-validator
```
Is the URL correct?

Use http://sigma-aetl-validator:8000 inside Docker

Use http://localhost:8000 from host

🧪 Does Swagger load?
```bash
curl http://localhost:8000/docs
```
✅ Validator must respond before testing the workflow.

📦 MongoDB Insert Fails (Duplicate Key Error)
Cause

machine_generated_id already exists

Idempotency is working as designed

Why this happens

Replay

Retry

Duplicate Kafka delivery

Manual re-execution

Resolution

🟢 No action required

🧠 This confirms exactly-once behavior at the application boundary

🧩 Index Errors in MongoDB
Symptom

Insert failures

Unexpected duplicates

Poor query performance

Required indexes

machine_generated_id (unique)

etl_metadata.machine_generated_id (unique / partial)

received_at (descending)

📌 If indexes are missing, idempotency is broken.

🧠 Ollama / AI Diagnostics Not Responding
Important

AI diagnostics are optional and non-blocking.

Symptoms

Ollama node errors

Model not found

Connection refused

Checks

Is Ollama installed?
```bash
ollama list
```
Is the model pulled?
```bash
ollama pull qwen2.5:7b
```
Safe behavior

🚫 AI failure does NOT break the pipeline

🚫 AI has NO authority over validation

✅ Core guarantees remain intact

🧪 Kafka Messages Not Triggering Workflow
Checks

Kafka container running

Correct topic name

Consumer group active

Message format is valid JSON

Reminder

Kafka is transport only, not truth.

All correctness is enforced downstream by the validator.

🧯 Docker Issues (Most Common Root Cause)
If things feel “weird”

Restart Docker Desktop

Ensure WSL2 backend is enabled

Verify enough memory allocated to Docker (≥ 8–12 GB)
```bash
docker compose down
docker compose up -d
```
Rule of thumb:
If Docker is healthy, SIGMA-AETL will behave deterministically.

🧠 Mental Model for Debugging

❝ If something fails loudly and predictably, the system is working. ❞

SIGMA-AETL is designed so that:

Validation failures are expected

Incorrect data never silently propagates

Replays are safe

Nothing is hidden

📎 When in Doubt

Inspect:

Validator response

MongoDB collections

n8n execution trace

Not logs.
Data.

That’s the contract-first mindset.
