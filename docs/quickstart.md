# ⚡ Quickstart — SIGMA-AETL v1.0

This guide walks you through a **minimal, end-to-end validation run** of SIGMA-AETL using the frozen **v1.0 contract**.

If everything works, you will:
- Ingest a valid payload → TRUE path → MongoDB
- Ingest an invalid payload → FALSE path → MongoDB
- Observe deterministic routing and idempotent behavior

⏱️ Estimated time: **10–15 minutes**

---

## 🧱 Prerequisites

You must already have:

- Docker Desktop running (WSL2 backend)
- This repository cloned locally
- No other services running on the same ports

If not, see [`docs/setup.md`](setup.md).

---

## 🚀 Step 1 — Start Infrastructure

From the repository root:

```bash
docker compose up -d
```
