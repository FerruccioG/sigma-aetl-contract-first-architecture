## 🧩 Minimum System Requirements (Realistic, Not Theoretical)

This is **not a toy stack** 🧸 — but it is also **not heavyweight** 🏋️.

---

### 🖥️ Operating System
- **Windows 11 64-bit**
  - ✅ Pro recommended (best Hyper-V / WSL2 stability)
  - ⚠️ Home edition works **only if WSL2 is enabled**

---

### 🧠 CPU
- **Minimum:** 4 cores / 8 threads (Intel i5 / Ryzen 5 class)
- **Recommended:** 6–8 cores 🚀  
- Kafka, Docker, and n8n **benefit from real parallelism**

---

### 🧬 Memory (RAM)
- **Minimum:** 16 GB  
- **Recommended:** 32 GB ✅  
  - 🐳 Docker (Kafka + MongoDB + n8n)
  - 🤖 Ollama model resident in memory
  - 🌐 Browser + IDE

> ⚠️ **8 GB will technically start**, but will be **unstable and frustrating**

---

### 💾 Storage
- **Minimum:** 50 GB free SSD
- **Recommended:** 100 GB SSD 🟢
  - 📦 Docker images
  - 🧾 Kafka logs
  - 🗄️ MongoDB data
  - 🤖 Ollama models (Qwen 7B ≈ 4–5 GB)

---

### 🎮 GPU (Optional — Not Required)
- ❌ **Not required**
- 🤖 Ollama runs CPU-only for diagnostics
- ⚡ GPU only improves **speed**, not **correctness**

---

## 🧰 Required Software Components

These are **hard requirements** — not optional suggestions.

---

### ⚙️ Core Runtime
- **Docker Desktop**
  - ✅ WSL2 backend enabled
  - Containers:
    - 📡 Kafka
    - 🧭 Zookeeper (or KRaft)
    - 🗄️ MongoDB
    - 🧠 n8n
    - 🛡️ SIGMA-AETL Validator

- **WSL2**
  - 🐧 Ubuntu 22.04 recommended
  - Used for:
    - Docker backend
    - CLI tooling
    - Kafka producer testing

---

### 📡 Data & Messaging
- **Apache Kafka**
  - Runs inside Docker 🐳
  - Used **strictly as transport**, never for validation

- **MongoDB**
  - Runs inside Docker 🐳
  - Collections:
    - ✅ `validated_shipments`
    - ❌ `failed_shipments`
  - 🔒 Unique indexes required for idempotency

---

### 🧠 Orchestration
- **n8n**
  - Runs inside Docker 🐳
  - Workflow imported from repo
  - Acts as:
    - Kafka consumer
    - Orchestration engine
    - TRUE/FALSE execution controller

---

### 🛡️ Validation Layer
- **SIGMA-AETL Validator**
  - ⚡ FastAPI + Pydantic
  - Runs in Docker
  - Exposes `/api/validate`
  - 🧾 Enforces **contract-first ingestion**

---

### 🤖 AI Diagnostics (Optional but Documented)
- **Ollama**
  - Installed on host (Windows or WSL)
  - Pulls `qwen2.5:7b`
  - Used **only** in FALSE branch
  - 🧠 Advisory, non-blocking, non-authoritative

---

## 🧭 Installation Sequence (Critical Order)

> ⚠️ **Order matters.** Skipping steps causes confusion.

---

### 🟡 Phase 0 — Host Preparation
1. Enable **Virtualization** in BIOS 🧬
2. Install Windows 11 updates 🔄
3. Install WSL2:
   ```powershell
   wsl --install
