# 🧊 Versioning & Contract Discipline — SIGMA-AETL

SIGMA-AETL treats **versioning as a first-class architectural concern**, not a release afterthought.  
This document explains **what “contract frozen” means**, why in-place changes are forbidden, and how future versions are introduced safely.

---

## 🎯 Core Principle: Contract-First Versioning

SIGMA-AETL enforces **explicit data contracts at the ingestion boundary**.

Once a contract is released:

- ❄️ It is **immutable**
- 🚫 It must **never be edited in place**
- 📜 Its behavior is **guaranteed forever**

This applies to:
- Schemas
- Validation rules
- Routing semantics
- Idempotency guarantees

📌 **If behavior must change, the version must change.**

---

## 🧱 What “Contract Frozen” Means

For **SIGMA-AETL v1.0**:

- 🧊 Schemas in `schemas/v1/` are frozen
- 🧊 Validator behavior is frozen
- 🧊 n8n workflow logic is frozen
- 🧊 TRUE / FALSE semantics are frozen

🚫 No:
- Schema tweaks
- Field reinterpretations
- Validation relaxations
- Silent fixes

---

## ❌ Why In-Place Changes Are Forbidden

In-place edits create hidden risk:

- ❌ Silent breaking changes
- ❌ Inconsistent replays
- ❌ Undetectable data drift
- ❌ Loss of audit confidence

SIGMA-AETL explicitly rejects:
- “Just one small field change”
- “Backward-compatible” assumptions
- Heuristic version guessing

📌 **If a change matters, it deserves a new version.**

---

## 🧭 Version Introduction Strategy

New versions are introduced explicitly:

```text
schemas/
  v1/   ← frozen
  v2/   ← new contracts
```
Each version includes:

🆕 Independent schemas

🆕 Independent validator logic

🆕 Independent workflow (or branch)

🆕 Explicit routing configuration

Multiple versions may coexist safely.

🔁 Replay & Backward Compatibility

Because contracts are immutable:

🔄 Old data can be replayed safely

📜 Historical correctness is preserved

🧾 Audits remain reproducible

🧪 Test results remain meaningful

Replays are deterministic because:

Validation rules do not drift

Idempotency guarantees remain valid

Storage semantics do not change

🔀 Orchestration Implications

In n8n:

🧭 v1 workflows remain untouched

🧭 v2 workflows are introduced explicitly

🚦 Routing decisions are version-aware

❌ No dynamic contract switching

This avoids:

Runtime ambiguity

Hidden conditional logic

Version inference bugs

🧠 AI Diagnostics & Versioning

AI diagnostics are version-agnostic by design:

🧠 Advisory only

🧠 Reads normalized failure records

❌ Cannot influence validation

❌ Cannot bypass version rules

📌 Model changes do not require contract version bumps.

🧊 Why This Discipline Matters

This approach enables:

🛡️ Strong production guarantees

📈 Predictable system evolution

🧪 Reliable testing & replay

👥 Clear team ownership boundaries

🧠 Trustworthy ingestion pipelines

SIGMA-AETL favors boring correctness over clever shortcuts.

✅ Summary

❄️ Contracts are immutable

🆕 Changes require new versions

🔁 Replays are always safe

🚫 No hidden behavior changes

🧠 AI never alters correctness

Versioning is not metadata — it is architecture.
