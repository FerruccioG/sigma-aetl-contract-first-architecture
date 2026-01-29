# 🧪 Examples — Payload Samples for SIGMA-AETL

This folder contains **intentionally minimal, explicit payload examples** used to demonstrate how the SIGMA-AETL contract-first ingestion pipeline behaves under different conditions.

These examples are designed for:
- 🔍 Validation testing
- 🧠 Architectural understanding
- 🧪 Smoke testing (TRUE / FALSE paths)
- 📚 Educational purposes

---

## 📁 Files in This Folder

### ✅ `valid_payload.json`
A **contract-compliant payload** that:
- Passes Pydantic schema validation
- Follows all business rules
- Routes through the **TRUE** execution path
- Is persisted into `validated_shipments`

🟢 Expected outcome:
- Validator returns `PASSED`
- Workflow follows TRUE branch
- Document inserted into MongoDB
- Idempotency enforced via unique indexes

---

### ❌ `invalid_payload.json`
An **intentionally broken payload** that violates multiple contract rules at once.

This example is *designed to fail* and **must not be fixed**.

It demonstrates:
- Empty required fields
- Invalid numeric values
- Missing required attributes

🔴 Expected outcome:
- Validator returns `FAILED`
- Workflow follows FALSE branch
- Record persisted into `failed_shipments`
- Optional AI diagnostics may run (advisory only)

---

## 🧠 Why These Examples Exist

These payloads exist to reinforce several core SIGMA-AETL principles:

- 📜 **Contracts are enforced at ingestion**
- 🚫 **Invalid data is never silently dropped**
- 🔁 **Retries and replays are safe**
- 🧱 **Failures are first-class data**
- 🔍 **Observability is built-in, not bolted on**

---

## ⚠️ Important Notes

- These `.json` files contain **JSON only** — no comments, no explanations.
- All human-readable explanations live in this `README.md`.
- This separation mirrors the real system:
  - 📦 Payloads are strict
  - 🧠 Context lives outside the data

---

## 🧭 How to Use These Files

You can use these payloads to:
- Send test messages to Kafka
- Manually POST to the validator API
- Run n8n smoke tests
- Verify MongoDB persistence
- Demonstrate idempotency behavior

---

## 🧠 Mental Model

> “If a payload fails here, it would fail in production —  
> and that is exactly the point.”

SIGMA-AETL is designed to **make failure visible, explainable, and safe**.

---

## 🔁 Kafka CLI Examples (Transport-Level Testing)

These examples demonstrate **event ingestion via Kafka**, reinforcing that Kafka is **transport only**, not validation or truth.

> Kafka does not validate schemas.  
> Kafka does not enforce contracts.  
> Kafka only delivers bytes.

### ▶️ Produce a VALID payload

```bash
cat valid_payload.json | kafka-console-producer \
  --broker-list localhost:9092 \
  --topic sigma-aetl.shipments
```
Expected behavior:

Message consumed by n8n

Validator returns PASSED

Workflow follows TRUE branch

Data inserted into validated_shipments

▶️ Produce an INVALID payload
```bash
cat invalid_payload.json | kafka-console-producer \
  --broker-list localhost:9092 \
  --topic sigma-aetl.shipments
```
🔴 Expected behavior:

Message consumed by n8n

Validator returns FAILED

Workflow follows FALSE branch

Data inserted into failed_shipments

Optional AI diagnostics may execute (advisory only)

🌐 Validator API Tests (Direct Contract Enforcement)

These tests bypass Kafka entirely and validate contract enforcement in isolation.

✅ Validate a GOOD payload
```bash
curl -X POST http://localhost:8000/api/validate \
  -H "Content-Type: application/json" \
  --data @valid_payload.json
```
🟢 Expected response:
```json
{
  "status": "PASSED"
}
```
❌ Validate a BAD payload
```bash
curl -X POST http://localhost:8000/api/validate \
  -H "Content-Type: application/json" \
  --data @invalid_payload.json
```
🔴 Expected response:
```json
{
  "status": "FAILED",
  "reason": "Schema validation failed",
  "errors": [...],
  "received_payload": {...}
}
```
⚠️ Note:

HTTP status is 200 by design

Contract result is semantic, not transport-level

📊 MongoDB Verification (Persistence & Idempotency)

These queries verify exactly-once behavior and failure isolation.

🔍 Check validated records
```bash
use sigma_aetl
db.validated_shipments.find().sort({ received_at: -1 }).limit(5)
```
Expected:

Only schema-compliant payloads

Unique machine_generated_id

No duplicates on replays

🔍 Check failed records
```bash
db.failed_shipments.find().sort({ received_at: -1 }).limit(5)
```
Expected:

Full failure context

Original payload preserved

Validation errors stored

Optional AI diagnostics attached

🧱 Verify Idempotency (Critical)

Re-send the same payload multiple times.
```bash
# Reproduce the same message
cat valid_payload.json | kafka-console-producer \
  --broker-list localhost:9092 \
  --topic sigma-aetl.shipments
```
Then check:
```bash
db.validated_shipments.countDocuments({
  machine_generated_id: "<same-id>"
})
```
✅ Result must always be:
```text
1
```
If not → idempotency is broken.
🧠 Key Takeaways

Kafka = transport, not truth 🚚

Validation = deterministic and explicit 📜

TRUE and FALSE paths are equally important 🔀

Failures are data, not logs ❌📄

Replays are safe 🔁

Nothing is hidden 🧱

🧭 Mental Model

“If it fails here, it would fail in production —
and that is exactly what makes the system trustworthy.”

SIGMA-AETL is designed to fail loudly, persist failures, and remain correct under pressure.






