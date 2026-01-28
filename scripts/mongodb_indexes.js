/**
 * SIGMA-AETL v1.0
 * MongoDB index definitions enforcing idempotency, replay safety,
 * and production-grade query performance.
 *
 * These indexes are REQUIRED for correctness.
 */

if (db.getName() !== "sigma_aetl") {
  throw new Error("This script must be run against the sigma_aetl database");
}

use sigma_aetl;

/**
 * 1. Index workflow execution lineage
 * Used for tracing failures per n8n run / replay / incident analysis
 */
db.failed_shipments.createIndex(
  { workflow_run_id: 1 },
  { name: "workflow_run_id_1" }
);

/**
 * 2. Time-based access pattern
 * Supports dashboards, recent-failure queries, retention jobs
 */
db.failed_shipments.createIndex(
  { received_at: -1 },
  { name: "received_at_-1" }
);

/**
 * 3. Idempotency guard (application-level exactly-once)
 * Enforces uniqueness for machine-generated identifiers
 * Only applies when the identifier exists and is a string
 */
db.failed_shipments.createIndex(
  { "etl_metadata.machine_generated_id": 1 },
  {
    name: "etl_metadata.machine_generated_id_1",
    unique: true,
    partialFilterExpression: {
      "etl_metadata.machine_generated_id": {
        $exists: true,
        $type: "string"
      }
    }
  }
);

/**
 * 4. Kafka replay / forensic lookup index
 * Allows correlation of failed messages back to Kafka offsets
 * Sparse to avoid indexing non-Kafka-originated records
 */
db.failed_shipments.createIndex(
  {
    "kafka_metadata.topic": 1,
    "kafka_metadata.offset": 1
  },
  {
    name: "kafka_metadata.topic_1_kafka_metadata.offset_1",
    sparse: true
  }
);

use sigma_aetl;

/**
 * 1. Time-based access pattern
 * Used for analytics, freshness checks, and replay verification
 */
db.validated_shipments.createIndex(
  { received_at: -1 },
  { name: "received_at_-1" }
);

/**
 * 2. Idempotency enforcement
 * Guarantees exactly-once persistence semantics
 * Prevents duplicates under retries and replays
 */
db.validated_shipments.createIndex(
  { machine_generated_id: 1 },
  {
    name: "machine_generated_id_1",
    unique: true
  }
);


