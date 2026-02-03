HANDOVER DOCUMENT — SIGMA-AETL → MongoDB INSERT ISSUE (n8n)
1️⃣ Objective (Very Explicit)

We want MongoDB to persist a full diagnostic document produced by an n8n workflow, not just _id, into these collections:

validated_shipments (TRUE branch)

failed_shipments (FALSE branch)

Each insert must store the entire JSON document, including nested objects.

2️⃣ Exact Fields That MUST Be Stored in MongoDB

The MongoDB document must contain everything below (this is not optional):

Top-level fields
{
  "text": "...",
  "workflow_run_id": "30",
  "received_at": "2026-01-13T09:50:51.889-05:00",
  "validator_version": "v1.0.0",
  "source_system": "SIGMA-AETL",
  "pipeline_version": "v1.0.0",
  "log_level": "ERROR",
  "machine_generated_id": "...",
  "elapsed_ms": "NaN",
  "is_retry": false,
  "env": "dev",
  "validator_latency_class": "NORMAL",
  "failure_type": "BusinessRuleViolation",
  "raw_payload_hash": "...",
  "correlation_id": null,
  "topic": null,
  "cluster": null,
  "producer_version": null,
  "message_key": null,
  "published_at_utc": null,

Nested ETL metadata (critical)
  "etl_metadata": {
    "workflow_run_id": "30",
    "machine_generated_id": "...",
    "validator_version": "sigma-aetl-validator-v1",
    "sentinel_version": "sigma-sentinel-v1",
    "etl_timestamp_utc": "...",
    "diagnostic_summary": null,
    "diagnostic_details": null,
    "source_payload_raw": null,
    "is_valid": false,
    "transport_metadata": {
      "type": "manual",
      "internal": {
        "trigger": "n8n-manual-execution",
        "user": "Ferruccio",
        "timestamp": "..."
      }
    }
  }
}


👉 This full structure exists and is visible in n8n JSON output before MongoDB insertion.

3️⃣ Current Observed Behavior (The Core Failure)

Despite:

Successful workflow execution (all nodes green)

MongoDB connectivity confirmed

Correct database and collection names

No MongoDB errors

Documents being created

MongoDB only stores:

{ "_id": ObjectId("...") }


Or, in one failed experiment:

{
  "_id": ObjectId("..."),
  "=[object Object]": null
}


This proves:

Insert operation executes

Payload is not being mapped

MongoDB node drops all fields silently

4️⃣ Environment Details (Important)
MongoDB

Version: 7.0.28

Running in Docker

No authentication

TLS OFF

Verified via mongosh

Collections verified via show collections

Insert confirmed by _id generation

n8n

Self-hosted

MongoDB node version: 1.2 (Latest)

Insert → Document

Collection name correct

JSON input visible in MongoDB node

Tested both:

Execute Step

Execute Workflow

Tested with Execute Once ON/OFF

Tested with Retry OFF

Tested with clean collections

5️⃣ JSON Is Correct (Proven)

The upstream REAL JSON diagnostic node returns this exact structure:

return [{
  json: {
    ...input,
    etl_metadata
  }
}];


This JSON:

Is visible in Input panel

Is visible in Output panel

Survives multiple nodes

Is not mutated before MongoDB insert

So the JSON itself is not the problem.

6️⃣ What Has Already Been Tried (Exhaustively)
❌ Fields mapping

Leaving Fields empty → inserts _id only

Using ={{ $json }} → creates =[object Object]

Mapping individual fields manually → nulls

Mapping nested fields → ignored

❌ Raw JSON / JSON Input

Enabled / disabled where available

Behavior unchanged

❌ Collection name issues

Discovered accidental collection named "failed shipments"

Fixed naming

Dropped bad collections

Recreated clean collections

❌ MongoDB refresh / visibility

Verified via CLI

No caching issue

Inserts are real

7️⃣ Key Insight (Why This Is Hard)

The n8n MongoDB node UI is misleading:

“Fields” is not the document body

MongoDB Insert node does not clearly expose how to pass $json as the root document

No error is thrown when payload is discarded

The node silently inserts an empty document

This feels like:

Either a node bug

Or a missing required option

Or a wrong operation mode

8️⃣ What We Need From Claude (Very Specific Ask)

We need Claude to:

🎯 Identify the exact correct way to insert a full $json document into MongoDB using n8n’s MongoDB node

Specifically:

Is there a required hidden option (e.g. Document → Fields vs Raw)

Is this a known bug in MongoDB node ≥ v1.2

Is the correct approach:

a Code node with MongoDB driver

a HTTP call to MongoDB

a different MongoDB operation

Does n8n require:

return [{ json: { document: $json }}]


instead of $json directly?

Is the MongoDB node expecting a specific field name (e.g. document) internally?

If this is impossible via UI, what is the minimum working workaround that preserves schema integrity?

9️⃣ Constraints

Do NOT flatten the JSON

Do NOT stringify the JSON

Must preserve nested objects

Must work for both TRUE/FALSE branches

Must be production-safe

🔚 Summary for Claude (One Sentence)

“We have a valid, visible JSON payload in n8n, MongoDB inserts succeed but silently discard all fields except _id; please identify the exact correct MongoDB node configuration or required structure to insert the full $json document, or confirm if this is a node limitation/bug and propose the cleanest workaround.”
