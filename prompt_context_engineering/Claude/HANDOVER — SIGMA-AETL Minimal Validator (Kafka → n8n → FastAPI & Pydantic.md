HANDOVER — SIGMA-AETL Minimal Validator (Kafka → n8n → FastAPI/Pydantic)
0. Context (one paragraph)

We are building a Kafka-triggered n8n workflow that sends a structured JSON payload to a FastAPI validator service using Pydantic. The validator is intentionally strict and must remain so. The workflow is currently looping on HTTP 422 errors due to payload shape / encoding issues between n8n and FastAPI, not due to business logic or schema flaws.

1️⃣ What we are trying to achieve (EXPECTED OUTPUT)
🎯 Primary Objective

A Kafka message consumed by n8n must be:

Unwrapped

Normalized in a Code node

Sent as a JSON object to a FastAPI endpoint (POST /api/validate)

Accepted by Pydantic without modification to backend code

Return HTTP 200

Allow the workflow to proceed to:

TRUE branch → data enrichment / insert

FALSE branch → rejection handling

📦 Exact Payload Expected by FastAPI (conceptually)

FastAPI expects one JSON object, not a string, not nested incorrectly, not double-encoded.

Conceptual shape:

{
  "validator_payload": {
    "shipment_id": null,
    "weight_kg": null,
    "destination": null,
    "priority": null,
    "raw_payload": {
      "shipment_id": null,
      "weight_kg": null,
      "destination": null,
      "priority": null
    }
  },
  "kafka_metadata": {
    "topic": "sigma.failed_shipments",
    "partition": null,
    "offset": null,
    "key": null,
    "timestamp": null,
    "consumer_group": "n8n-sigma-aetl-validator"
  }
}


This is already produced correctly by the n8n Code node.

2️⃣ What has been tried so far (ALL attempts & outcomes)
✅ Backend (FastAPI / Pydantic)

Validator service works correctly

Logs show many successful 200 OK requests

When payload shape is wrong → Pydantic correctly returns 422 Unprocessable Entity

Backend must not be changed

❌ Failed / Problematic Attempts in n8n
Attempt 1 — RAW/Custom Body + JSON.stringify

Body Content Type: RAW/Custom

Body Parameters: JSON.stringify($json.validator_payload)

Result:

FastAPI receives stringified JSON

Pydantic error:

Input should be a valid dictionary


Outcome: ❌ Rejected

Attempt 2 — RAW/Custom Body + ={{ $json.validator_payload }}

Body Content Type: RAW/Custom

Result:

n8n sends [object Object]

Pydantic error:

Input should be a valid dictionary
Input: "[object Object]"


Outcome: ❌ Rejected

Attempt 3 — RAW/Custom Body + ={{ $json }}

Body Content Type: RAW/Custom

Result:

Double-encoding / string coercion

Outcome: ❌ Rejected

Attempt 4 — Manual Headers (Content-Type: application/json)

Headers explicitly set

Result:

n8n conflicts with internal request handling

Error:

Cannot create property 'accept' on string


Outcome: ❌ Rejected

Attempt 5 — Switching between

={{ $json.validator_payload }}

={{ $json }}

JSON.stringify(...)

Headers on/off

RAW/Custom vs JSON

All combinations led to either:

string payload

[object Object]

or double-encoded JSON

Core symptom never changed:

422 Unprocessable Entity
Input should be a valid dictionary

3️⃣ What is CONFIRMED to be correct

✔ Kafka trigger works
✔ Code node output is structurally correct
✔ Validator service works
✔ Pydantic schema works
✔ Network connectivity works
✔ n8n workflow activation works

The only failing layer is n8n HTTP node body serialization

4️⃣ What assistance is REQUIRED from Claude (very specific)

We need Claude to do ONE of the following, clearly and decisively:

🔧 Option A — Canonical n8n HTTP Node Configuration

Provide the exact, correct, minimal n8n HTTP node configuration that:

Sends the entire incoming item as JSON

Does not stringify

Does not nest incorrectly

Is compatible with FastAPI + Pydantic

This must include:

Body Content Type

JSON/RAW Parameters toggle

Exact Body Parameters (key/value)

Headers (if any)

Explanation of why this works in n8n’s internals

🔍 Option B — Identify n8n Limitation / Bug

If the configuration we expect cannot work due to:

Known n8n v2.x HTTP node behavior

A documented serialization quirk

A bug related to RAW/JSON switching

Then Claude must:

Explicitly say so

Cite or explain the limitation

Propose a workaround that does NOT weaken validation
(e.g., wrapper endpoint, adapter node, pre-flight transform)

🚫 What Claude should NOT do

Do NOT suggest relaxing Pydantic

Do NOT suggest accepting strings

Do NOT suggest removing validation

Do NOT suggest backend changes unless strictly unavoidable

Do NOT re-explain Kafka or FastAPI basics

5️⃣ Definition of “Done”

This task is complete when:

HTTP node consistently returns 200

No 422 appears in validator logs

Payload arrives as a dictionary, not string

Workflow proceeds beyond validator node

6️⃣ Tone & Intent

We are past exploration.
We are now in resolution mode.

The goal is to lock the correct pattern once, document it, and move forward with the SIGMA-AETL pipeline.
