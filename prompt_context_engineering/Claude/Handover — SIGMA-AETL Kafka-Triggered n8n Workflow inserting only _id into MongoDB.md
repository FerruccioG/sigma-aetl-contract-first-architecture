Claude Handover — SIGMA-AETL Kafka-Triggered n8n Workflow inserting only _id into MongoDB
Context / Objective

We migrated an n8n workflow from Manual Trigger to Kafka Trigger (topic sigma.failed_shipments) and want to persist records into MongoDB with full payload + Kafka transport metadata.

We want each Mongo document to include at minimum:

root_cause

missing_or_invalid_fields

why_it_failed

proposed_fix

business_implication

workflow_run_id

received_at

validator_version

source_system

pipeline_version

log_level

etl_metadata (nested)

transport_metadata with Kafka details (nested)

Target schema expectation inside MongoDB:

{
  root_cause: "...",
  missing_or_invalid_fields: [...],
  why_it_failed: "...",
  proposed_fix: "...",
  business_implication: "...",
  workflow_run_id: "...",
  received_at: "...",
  validator_version: "...",
  source_system: "...",
  pipeline_version: "...",
  log_level: "...",
  etl_metadata: { ... },
  transport_metadata: {
    type: "kafka",
    kafka: {
      topic: "...",
      partition: <number>,
      offset: <number>,
      key: <string|null>,
      consumer_group: "n8n-sigma-aetl-validator",
      timestamp: <string ISO optional>
    }
  }
}

Environment

Docker compose stack on Linux VM:

n8n v2.1.4

kafka confluentinc/cp-kafka:7.5.0 on port 9092

zookeeper

mongo:7.0 container sigma-mongodb

sigma-aetl-validator (FastAPI)

ollama

Kafka exists and works inside container. Host VM does not have Kafka CLI installed; Kafka CLI is used via docker exec -it kafka bash.

Kafka topic:

sigma.failed_shipments

Consumer group observed:

n8n-sigma-aetl-validator

What works

Kafka Trigger works

n8n Kafka credentials set with:

Brokers: kafka:9092

SSL OFF (SSL ON caused TLS disconnect error; OFF passed)

Authentication OFF

Trigger listens and fires when a message is produced.

MongoDB Insert node connectivity works

Insert node returns _id in output.

Same _id found in MongoDB collection, proving insertion succeeded.

The main problem (symptom)

When Insert Documents node is configured with Fields = EMPTY, it inserts only an empty document and MongoDB returns _id. Querying Mongo shows documents as:

{ _id: ObjectId("...") }


We want the full document inserted, not {}.

Observed side effects / weird docs

At times, the collection had bad documents like:

{ _id: ..., '=[object Object]': null }


This happened during earlier attempts when Fields mapping was wrong or strings were pasted into “Fields” box.

Current workflow nodes of interest (conceptual)

Kafka Trigger

Unwrap Kafka Message (Code node) — unwraps/parses Kafka message

POST → SIGMA-AETL Validator (HTTP)

If (valid / invalid)

Failure branch includes LLM Sentinel, Parse, Inject Kafka Metadata, Normalize JSON document, Insert documents1 (MongoDB)

Attempts we made so far (and what they proved)
A) Kafka credential tests

SSL ON → “Client network socket disconnected before secure TLS connection established”

SSL OFF → connection success

✅ Conclusion: broker is PLAINTEXT; SSL must stay OFF.

B) Triggering Kafka

We produced messages via:

docker exec -it kafka bash
kafka-console-producer --bootstrap-server kafka:9092 --topic sigma.failed_shipments
{ "shipment_id":"SHIP-2026-001", "schema_version":"1.0", "status":"FAILED", "error":"missing_required_field" }


Also consumed via:

kafka-console-consumer --bootstrap-server kafka:9092 --topic sigma.failed_shipments --from-beginning --max-messages 1


✅ Conclusion: message produced; trigger consumes.

C) Adding Unwrap Kafka Message node

Initially it threw “Invalid time value [line 17] RangeError” because code tried:

new Date(msg.timestamp).toISOString()


but timestamp wasn’t valid / present.

We corrected by removing or guarding timestamp conversion, and node became green.

✅ Conclusion: Kafka Trigger item structure may not always include a valid timestamp field; must guard.

D) Transport metadata missing in MongoDB

We queried:

db.failed_shipments.find(
  { "transport_metadata.type": "kafka" },
  { transport_metadata: 1, _id: 0 }
).sort({ received_at: -1 }).limit(1).pretty()


Returned nothing.

At that stage, stored docs had transport_metadata = manual (from old flow) or null. Even after Kafka triggering, payload still showed manual metadata because our normalize node kept etl_metadata.transport_metadata from validator stage or null.

We created / discussed a node called “Inject Kafka Metadata” to add:

transport_metadata: {
  type: "kafka",
  kafka: {...}
}


However, later we disabled “Inject Kafka Metadata” during testing, so Kafka metadata never made it to Mongo.

✅ Conclusion: To get Kafka metadata in Mongo, we must explicitly merge Kafka trigger info into the output JSON BEFORE Insert.

E) “Normalize JSON document” node

Current/previous code (user-provided):

const input = $json;
const kafka_metadata = input.kafka_metadata || null;

return [{
  json: {
    root_cause: input.root_cause,
    missing_or_invalid_fields: input.missing_or_invalid_fields,
    why_it_failed: input.why_it_failed,
    proposed_fix: input.proposed_fix,
    business_implication: input.business_implication,

    workflow_run_id: input.workflow_run_id,
    received_at: input.received_at,
    validator_version: input.validator_version,
    source_system: input.source_system,
    pipeline_version: input.pipeline_version,
    log_level: input.log_level,

    etl_metadata: input.etl_metadata,
    kafka_metadata
  }
}];


Notes:

It outputs kafka_metadata not transport_metadata.

It may preserve manual transport inside etl_metadata.transport_metadata, but top-level transport_metadata often becomes null.

Mongo queries look for transport_metadata.type = kafka, but we aren’t writing it.

✅ Conclusion: Normalizer must produce top-level transport_metadata with Kafka structure (or we must re-enable Inject Kafka Metadata).

F) MongoDB Insert node behaviour

Critical observation:

With Fields EMPTY, output is only _id and Mongo doc is {_id:...}.

Therefore the node is inserting an empty document, not the incoming JSON.

We repeatedly returned to “Fields EMPTY” due to earlier assumptions that EMPTY means “insert all incoming fields”. In this n8n version/node, EMPTY does NOT do that. It inserts {} unless fields are mapped.

✅ Conclusion: Fields EMPTY is the root cause of “only _id inserted”.

What we need from Claude (explicit asks)
1) Confirm n8n MongoDB node semantics in v2.1.4

We need Claude to confirm definitively:

In the MongoDB node (Resource: Document, Operation: Insert), does “Fields empty” insert {}?

If yes, what is the correct configuration to insert the entire $json as the document?

2) Provide the correct Insert node configuration (step-by-step)

We need a deterministic recipe that results in inserting the full JSON.

We are open to either:

Mapping a single field like payload: {{$json}} (wrap)
or

Inserting raw JSON if supported by this node/version (no wrap)

But we need:

exact node settings

exact expression(s)

example of resulting Mongo document

3) Ensure Kafka metadata is preserved and queryable

We need Claude to specify how to carry Kafka metadata into Mongo.

Acceptance criteria:

After inserting, this query returns at least 1 document:

db.failed_shipments.find(
  { "transport_metadata.type": "kafka" },
  { transport_metadata: 1, _id: 0 }
).sort({ received_at: -1 }).limit(1).pretty()


We need Claude to specify:

where to create transport_metadata (Unwrap? Inject node? Normalize node?)

how to map Kafka trigger output fields reliably (topic/partition/offset/key/group/timestamp)

guardrails for nulls

4) Fix the “=[object Object]”: null documents issue

We want Claude to explain precisely:

how those docs get created (bad mapping?)

how to prevent it

optionally, a cleanup query to remove corrupted docs

5) Provide a recommended final architecture for this pipeline

We want the cleanest approach:

Unwrap Kafka message → parse JSON payload

build a canonical document containing payload + transport metadata

insert into Mongo

We want this standardized so we can freeze DEV and move to PROD.

Current state right now (latest)

Kafka Trigger works.

Unwrap Kafka Message works.

“Inject Kafka Metadata” is currently disabled in latest test run.

Normalize JSON node outputs fields + kafka_metadata: null (because not injected).

Mongo insert with Fields EMPTY inserts only _id (confirmed by Mongo query).

This is the core blocker.

Deliverable requested from Claude

The exact configuration of Mongo Insert to insert full JSON (NOT just _id)

The exact JS code (or node expressions) to create top-level:

transport_metadata: { type: "kafka", kafka: {...} }


A minimal smoke test procedure (produce message → verify Mongo query)

Explanation of how to avoid “=[object Object]” corruption docs
