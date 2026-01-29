1️⃣ Full workflow overview

Shows Kafka → Validator → IF → TRUE / FALSE

Highlights frozen contract note

2️⃣ TRUE branch execution

Validator PASSED

Insert into validated_shipments

3️⃣ FALSE branch execution

Validator FAILED

AI diagnostic node (optional)

Insert into failed_shipments

4️⃣ Execution log details

Show deterministic branching

No retries causing duplicates

🔐 Security & Trust Boundaries
🧱 Explicit Trust Model

| Component | Trust Level | Responsibility    |
| --------- | ----------- | ----------------- |
| Kafka     | ❌ Untrusted | Transport only    |
| Producers | ❌ Untrusted | Emit payloads     |
| Validator | ✅ Trusted   | Enforce contracts |
| n8n       | ✅ Trusted   | Orchestration     |
| MongoDB   | ✅ Trusted   | Persistence       |
| AI Agent  | ❌ Untrusted | Advisory only     |

🧠 AI Safety Model

AI runs only on FAILED data

Cannot influence control flow

Cannot mutate records

Can be removed without breaking pipeline

AI augments understanding — it never defines correctness.

🧭 Final Mental Model

Correctness is enforced at the boundary.
Everything downstream assumes the contract was honored.

SIGMA-AETL is not optimized for convenience.
It is optimized for truth, traceability, and survival under failure.
