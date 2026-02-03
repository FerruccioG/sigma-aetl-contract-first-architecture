# ⚡ Quickstart — SIGMA-AETL v1.0

This guide walks you through a **minimal, end-to-end validation run** of SIGMA-AETL using the frozen **v1.0 contract**.

If everything works, you will:
- Ingest a valid payload → TRUE path → MongoDB
- Ingest an invalid payload → FALSE path → MongoDB
- Observe deterministic routing and idempotent behavior

⏱️ Estimated time: **10–15 minutes**

---

## 🧱 Prerequisites

You must already have:

- Docker Desktop running (WSL2 backend)
- This repository cloned locally
- No other services running on the same ports

If not, see [`docs/setup.md`](setup.md).

---

## 🚀 Step 1 — Start Infrastructure

From the repository root:

```bash
docker compose up -d
```
This starts:

Kafka

MongoDB

Redis

n8n

SIGMA-AETL Validator

Verify containers:
```bash
docker ps
```
All containers should be running.

Step 2 — Verify Validator Is Alive
```bash
http://localhost:8000/docs
```
You should see the FastAPI Swagger UI.

✅ If this page loads, validation is reachable.

Step 3 — Create MongoDB Indexes (Mandatory)

Connect to MongoDB:
```bash
docker exec -it sigma-mongodb mongosh
```
Select database:
```js
use sigma_aetl
```
Create indexes:
```js
// Validated shipments (idempotency)
db.validated_shipments.createIndex(
  { machine_generated_id: 1 },
  { unique: true }
)

// Failed shipments (idempotency + sparse)
db.failed_shipments.createIndex(
  { "etl_metadata.machine_generated_id": 1 },
  {
    unique: true,
    partialFilterExpression: {
      "etl_metadata.machine_generated_id": { $exists: true, $type: "string" }
    }
  }
)

// Operational queries
db.failed_shipments.createIndex({ received_at: -1 })
db.validated_shipments.createIndex({ received_at: -1 })
```
Without these indexes, idempotency is broken.

🧩 Step 4 — Import n8n Workflow

Open n8n UI
👉 http://localhost:5678

Import workflow:

File: orchestration/n8n/sigma-aetl-v1.json

Verify workflow header:

“Production pipeline. Contract frozen at SIGMA-AETL v1.0. Do not modify without version bump.”

Activate the workflow

✅ Step 5 — TRUE Payload Test

Send a valid payload:

```json
{
  "shipment_id": "SHIP-TRUE-001",
  "weight_kg": 12.5,
  "destination": "Dublin",
  "priority": 2
}
```
Expected behavior:

Validator returns PASSED

Workflow follows TRUE branch

Document inserted into validated_shipments

Verify:
```js
db.validated_shipments.find({ shipment_id: "SHIP-TRUE-001" }).pretty()
```
❌ Step 6 — FALSE Payload Test

Send an invalid payload:
```js
{
  "shipment_id": "",
  "weight_kg": -5,
  "destination": "Dublin"
}
```
Expected behavior:

Validator returns FAILED

Workflow follows FALSE branch

Document inserted into failed_shipments

Optional AI diagnostics enrichment (if Ollama is enabled)

Verify:
```js
db.failed_shipments.find().sort({ received_at: -1 }).limit(1).pretty()
```
Optional — AI Diagnostics

If Ollama is installed:
```bash
ollama pull qwen2.5:7b
```
The AI diagnostics node:

Runs only on FAILED payloads

Is advisory

Never blocks or alters execution

🎯 Success Criteria

You are done when:

TRUE payload reaches validated_shipments

FALSE payload reaches failed_shipments

No retries create duplicates

No payload bypasses validation

🧊 Notes

This workflow is contract-frozen

Do not modify in place

Any change requires a version bump (v2)

For deeper explanation, see:

docs/setup.md

docs/versioning.md

architecture/



