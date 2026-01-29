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
Happy testing 🚀
