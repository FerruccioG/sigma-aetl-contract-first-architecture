HANDOVER REPORT — SIGMA-AETL Kafka → n8n → MongoDB Pipeline
1. Objective (What We Are Building)

We are building a Kafka-triggered ETL validation pipeline using n8n that:

Consumes messages from Kafka topic:

sigma.failed_shipments


Each Kafka message is a JSON payload representing a failed shipment event.

The workflow:

Unwraps the Kafka message

Sends payload to a SIGMA-AETL Validator (HTTP)

Routes:

✅ Valid → clean transform → MongoDB

❌ Invalid → AI Sentinel (LLM) → structured error document → MongoDB

Failed shipments originating from Kafka must be stored in MongoDB with:

"transport_metadata": {
  "type": "kafka",
  ...
}


This is a production-style Kafka consumer workflow, not a manual test workflow.

2. Current Architecture (n8n Workflow)

Workflow name

SIGMA-AETL Minimal Validator Test – v2 (DEV – Kafka Triggered)


Core nodes

Kafka Trigger

Unwrap Kafka Message (JS)

POST → SIGMA-AETL Validator (HTTP)

IF (status === PASSED)

TRUE branch → Transform → MongoDB insert

FALSE branch:

SIGMA-AETL Sentinel (LLM)

Parse Text

Attach ETL Metadata

Normalized JSON document

MongoDB insert (failed_shipments)

Important

The workflow JSON is correct

All data-shape bugs were fixed

MongoDB inserts work when workflow is manually executed

3. What Works (Confirmed with Evidence)
✅ Kafka Infrastructure

Kafka broker is healthy

Topic exists: sigma.failed_shipments

Messages are produced successfully

Messages are consumed by CLI consumers

Example produced message:

{
  "shipment_id": "KAFKA-REAL-001",
  "schema_version": "1.0",
  "status": "FAILED",
  "error": "missing_destination"
}

✅ n8n Kafka Trigger Configuration

Correct topic

Correct group ID: n8n-sigma-aetl-validator

Kafka Trigger receives messages when manually tested

Kafka Trigger output shows:

{
  "message": "{...json string...}",
  "topic": "sigma.failed_shipments"
}

✅ Unwrap Kafka Message Node

Correctly parses JSON string into object

Adds kafka_metadata correctly

Output verified and correct

✅ Downstream Logic

Validator routing works

AI Sentinel works

Normalized JSON document works

MongoDB insert works

✅ MongoDB

Collection: failed_shipments

Documents insert correctly

Historical manual records exist

4. What Does NOT Work (The Blocking Issue)
❌ Kafka Trigger Does NOT fire automatically

Symptoms

Sending Kafka messages produces NO new n8n execution

MongoDB does NOT receive new Kafka-sourced documents

transport_metadata.type = kafka never appears

Kafka consumer group offsets do not move due to n8n

❌ Workflow never shows “Active”

Top-right of n8n UI only shows:

Saved
Publish


There is NO Active / Inactive toggle visible.

This means:

Kafka Trigger is NOT running as a background consumer

5. Critical Observation

In n8n:

Kafka Triggers ONLY run when a workflow is ACTIVE

“Saved” or “Published” alone is not sufficient

Without Active = ON, Kafka messages are ignored

However:

In this n8n instance, the Active toggle does not appear at all

This is the core blocker.

6. Tests Already Performed (To Avoid Re-testing)

✔ Reset Kafka offsets
✔ Verified consumer group
✔ Produced new Kafka messages
✔ Verified topic consumption via CLI
✔ Unpinned Kafka Trigger
✔ Restarted workflow executions
✔ Verified payload formats
✔ Verified Unwrap logic
✔ Verified MongoDB writes on manual execution

All of the above are confirmed working.

This is not a data, schema, or Kafka issue.

7. What We Need Help With (Explicit Ask to Claude)
🎯 Primary Question

Why does this n8n instance NOT show an Active toggle for Kafka Trigger workflows?

🎯 Specific Areas We Need Claude’s Help On

n8n deployment mode analysis

Is this instance running in:

editor-only mode?

queue mode without workers?

webhook-only mode?

Kafka Trigger lifecycle

What conditions must be met for Kafka Trigger to register a consumer?

Is activation disabled at instance level?

UI vs backend mismatch

Is there a known issue where Active toggle is hidden?

Does Kafka Trigger require:

n8n Cloud?

specific license?

background workers?

Config-level checks

Environment variables that disable triggers

EXECUTIONS_MODE

QUEUE_* settings

Docker flags

How to force activation

CLI activation

API activation

DB-level workflow activation

Minimal reproducible test

What is the absolute smallest Kafka Trigger workflow that should activate?

How to verify consumer is running internally

8. What We Are NOT Asking For

No workflow redesign

No schema changes

No Kafka reconfiguration

No MongoDB changes

No payload changes

This is purely an n8n trigger lifecycle / activation problem.

9. Deliverables Requested from Claude

Root cause explanation

Exact reason Active toggle is missing

Step-by-step fix

How to verify Kafka Trigger is truly running

Best-practice n8n Kafka deployment guidance

10. Attachments

Full workflow JSON (to be attached separately)

Screenshots showing:

No Active toggle

Kafka Trigger output

MongoDB verification

Kafka CLI producer/consumer tests

11. Final Status Summary
Component	Status
Kafka	✅ Working
n8n workflow logic	✅ Correct
MongoDB	✅ Working
Kafka Trigger	❌ Not activated
Root cause	🔴 n8n trigger lifecycle / instance configuration
Closing Note to Claude

This pipeline is functionally correct.
The only missing piece is Kafka Trigger activation at the n8n instance level.
Please focus on why activation is impossible in this environment and how to enable it.
