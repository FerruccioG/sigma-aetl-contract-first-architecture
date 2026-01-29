📘 SIGMA-AETL Architecture Documentation

This folder contains structured documentation explaining the contract-first, event-driven architecture behind SIGMA-AETL 🧱🚀

You’ll find:

🔐 Why validation happens at the ingestion boundary

🔄 How data flows from Kafka → Validator → TRUE/FALSE paths → MongoDB

❌ Why failures are first-class citizens (not logs)

♻️ How idempotency and safe replays are guaranteed

🧠 Where AI-assisted diagnostics fit — and where they don’t

The goal is architectural clarity: helping readers understand the tradeoffs, constraints, and guarantees that make the system production-safe under real-world conditions ⚙️📈
