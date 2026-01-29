
# 🧪 Smoke Tests — SIGMA-AETL v1.0

This document describes the **mandatory smoke tests** required to validate that the SIGMA-AETL contract-first ingestion pipeline is functioning correctly end-to-end.

These tests verify:
- ✅ Contract enforcement at ingestion
- 🔀 Deterministic TRUE / FALSE routing
- ♻️ Idempotent persistence
- 📦 Correct MongoDB writes
- 🤖 Optional AI diagnostics behavior

---

## 🎯 Purpose of Smoke Tests

Smoke tests are **not optional**.

They ensure that:
- The validator is authoritative
- Invalid data never contaminates validated datasets
- Replays are safe
- Failures are first-class citizens

If any test below fails, **do not proceed** with further experimentation.

---

## ✅ Test 1 — TRUE Payload (Valid Contract)

### 📥 Input Payload

```json
{
  "shipment_id": "SHIP-TRUE-001",
  "weight_kg": 12.5,
  "destination": "Dublin",
  "priority": 2
}
```
🔄 Expected Behavior

Validator returns status = PASSED

Workflow follows the TRUE branch

Payload is transformed and normalized

Record is inserted into validated_shipments

machine_generated_id is unique

MongoDB Verification
```js
db.validated_shipments.find({
  shipment_id: "SHIP-TRUE-001"
}).pretty()
```
Success Criteria

Exactly one document inserted

All required fields present

No duplicate records on replay

Test 2 — FALSE Payload (Schema Violation
```json
{
  "shipment_id": "",
  "weight_kg": -5,
  "destination": "Dublin"
}
```

🔄 Expected Behavior

Validator returns status = FAILED

Workflow follows the FALSE branch

Payload is normalized into a failure schema

Record is inserted into failed_shipments

No write occurs to validated_shipments

📦 MongoDB Verification
```js
db.failed_shipments.find().sort({ received_at: -1 }).limit(1).pretty()
```
✅ Success Criteria

Failure record persisted

Validation errors captured

is_valid = false

Failure data is indexed and queryable

♻️ Test 3 — Idempotency / Replay Safety
🔁 Action

Re-submit the same TRUE payload multiple times.

🔄 Expected Behavior

Validator continues to PASS

MongoDB rejects duplicates

No additional records inserted

📦 MongoDB Verification

```js
db.validated_shipments.countDocuments({
  shipment_id: "SHIP-TRUE-001"
})
```
✅ Success Criteria

Count remains 1

No duplicate data

No manual cleanup required

🤖 Test 4 — AI Diagnostics (Optional)

This test applies only if Ollama is enabled.

🔄 Expected Behavior

AI agent runs only on FALSE branch

Provides advisory diagnostics

Does not influence routing or correctness

Pipeline continues regardless of AI availability

✅ Success Criteria

Failure persists even if AI is disabled

AI output is informational only

No execution dependency on the model

🚫 What Must NEVER Happen

❌ Invalid payload reaches validated_shipments

❌ Validator decision overridden downstream

❌ Failures logged but not persisted

❌ Duplicate data on replay

❌ AI influencing ingestion decisions

If any of the above occurs, the system is misconfigured.

🧠 Final Assertion

If all tests pass:

The ingestion boundary is hardened.
The contract is enforced.
Replays are safe.
Failures are first-class.

This confirms SIGMA-AETL v1.0 is operating as designed.


