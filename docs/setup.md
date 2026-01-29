# 🛠️ SIGMA-AETL — Local Setup Guide (Windows 11)

This guide explains how to install, run, and validate the **SIGMA-AETL contract-first ingestion pipeline** on a local Windows 11 machine.

This is a **realistic production-style stack**, not a toy demo — but it is deliberately kept **self-contained and reproducible**.

---

## 💻 Minimum System Requirements (Realistic, Not Theoretical)

This stack is demanding, but intentionally so.

### 🪟 Operating System
- Windows 11 64-bit
- **Pro recommended** (better Hyper-V / WSL2 stability)
- Home edition works **if WSL2 is enabled**

### 🧠 CPU
- **Minimum:** 4 cores / 8 threads (Intel i5 / Ryzen 5 class)
- **Recommended:** 6–8 cores
- Kafka + Docker + n8n benefit heavily from parallelism

### 🧮 Memory (RAM)
- **Minimum:** 16 GB  
- **Recommended:** 32 GB  

Includes:
- Docker containers (Kafka, MongoDB, n8n)
- Validator service
- Ollama model resident in memory
- Browser + IDE

👉 **8 GB will technically start**, but will be unstable and frustrating.

### 💾 Storage
- **Minimum:** 50 GB free SSD
- **Recommended:** 100 GB SSD

Used by:
- Docker images
- Kafka logs
- MongoDB data
- Ollama models (Qwen 7B ≈ 4–5 GB)

### 🎮 GPU (Optional)
- ❌ Not required
- Ollama runs CPU-only perfectly fine
- GPU only improves diagnostic latency, **not correctness**

---

## 🔌 Local Ports Used

| Service        | Port  |
|---------------|-------|
| n8n           | 5678  |
| Validator API | 8000  |
| Kafka         | 9092  |
| MongoDB       | 27017 |

---

## 📦 Required Software Components

These are **hard requirements**, not optional suggestions.

### 🧱 Core Runtime
- **Docker Desktop**
  - WSL2 backend enabled
  - Docker Compose v2 enabled

- **WSL2**
  - Ubuntu 22.04 recommended
  - Used for:
    - Docker backend
    - CLI tooling
    - Kafka producer testing

---

### 📡 Data & Messaging
- **Apache Kafka**
  - Runs inside Docker
  - Used strictly as *transport*, not validation

- **MongoDB**
  - Runs inside Docker
  - Collections:
    - `validated_shipments`
    - `failed_shipments`
  - Requires **unique indexes** for idempotency

---

### 🧩 Orchestration
- **n8n**
  - Runs inside Docker
  - Workflow imported from this repo
  - Acts as:
    - Kafka consumer
    - Orchestration engine
    - Branching controller

---

### 🛂 Validation Layer
- **SIGMA-AETL Validator**
  - FastAPI + Pydantic
  - Runs in Docker
  - Exposes `/api/validate`
  - Enforces **contract-first ingestion**

---

### 🤖 AI Diagnostics (Optional, Non-Blocking)
- **Ollama**
  - Installed on host (Windows or WSL)
  - Pulls `qwen2.5:7b`
  - Used **only in FAILED branch**
  - Advisory, non-authoritative

⚠️ First Ollama model pull may take several minutes depending on bandwidth.

---

## 🧭 Installation Sequence (Critical Order)

⚠️ **Order matters. Skipping steps causes confusion.**

---

### Phase 0 — Host Preparation 🧰

1. Enable virtualization in BIOS
2. Install all Windows 11 updates
3. Install WSL2:
   ```bash
   wsl --install

Install Docker Desktop

Enable:

✅ WSL2 backend

✅ Docker Compose v2

✅ Success check:

Docker Desktop starts cleanly

No startup errors

🛑 Stop here if Docker cannot start.

Phase 1 — Infrastructure Containers 🧱

Clone the GitHub repository

Start base infrastructure:

docker compose up -d


This brings up:

Kafka

Zookeeper (or KRaft)

MongoDB

Redis (n8n)

n8n

Verify:

docker ps


✅ Success check:

All containers running

No restart loops

Phase 2 — Validator Service 🛂

Build validator image:

docker build -t sigma-aetl-validator:local .


Start validator:

docker compose up -d sigma-aetl-validator


Verify:

curl http://localhost:8000/docs


✅ Success check:

Swagger UI loads

/api/validate visible

🛑 Validator must respond before n8n testing.

Phase 3 — MongoDB Indexes (Mandatory) 🧷

Connect to MongoDB:

docker exec -it sigma-mongodb mongosh


Create required indexes:

machine_generated_id (unique)

etl_metadata.machine_generated_id (partial unique)

received_at (descending)

👉 Without these indexes, idempotency is broken.

✅ Success check:

getIndexes() shows all required indexes

Phase 4 — n8n Workflow Setup 🔄

Open n8n UI:

http://localhost:5678


Import workflow JSON from repo

Configure credentials:

Kafka

HTTP (Validator)

MongoDB

Ollama (optional)

Activate workflow

✅ Success check:

Workflow activates without errors

Kafka trigger shows connected

Phase 5 — AI Diagnostics (Optional) 🤖

Install Ollama

Pull model:

ollama pull qwen2.5:7b


Verify:

ollama list


✅ Success check:

Model listed locally

Ollama responds to prompts

Phase 6 — Smoke Tests (Required) 🧪
✅ TRUE Payload

Passes validator

Follows TRUE branch

Inserts into validated_shipments

❌ FALSE Payload

Fails validator

Follows FALSE branch

Inserts into failed_shipments

Optional AI enrichment applied

✅ Success check:

Both collections populated correctly

No duplicate inserts on replay

🚫 What This Setup Intentionally Does NOT Require

❌ Kubernetes

❌ Spark

❌ Airflow

❌ Cloud services

❌ GPU

❌ Paid APIs

❌ External AI providers

This system is deliberately self-contained.

🧠 Mental Model for New Users

“If Docker works, everything else is configuration and discipline.”

This architecture guarantees that:

Validation is deterministic ✅

Failures are first-class citizens ❌

Replays are safe 🔁

Nothing is hidden 🧾

Welcome to contract-first ingestion.

---

If you want, tomorrow we can:

- 🔍 Cross-check **Linux VM ↔ Docker ↔ n8n wiring**
- 🧪 Re-run TRUE/FALSE payloads against this guide
- 🧭 Add a **one-page architecture walk-through for recruiters**

You closed today at a *very* strong checkpoint.
::contentReference[oaicite:0]{index=0}
