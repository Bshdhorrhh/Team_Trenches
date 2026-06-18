# 🚀 DeepThinker — Startup Guide

> **Prerequisites:** Ensure you have completed the one-time installation steps in [README_SETUP.md](./README_SETUP.md) first.

---

## ⚡ Method 1: One-Command Start (Linux Only — `start.sh`)

For Ubuntu/Linux users, the easiest way to start is with the provided shell script:

```bash
bash start.sh
```

The script will:
1. Kill any leftover processes from previous runs on ports `8000` and `5173`
2. Set Intel iGPU environment variables automatically
3. Launch the backend and verify it is actually running before starting the frontend
4. Print `🟢 Both servers are running!` when everything is healthy

> ⚠️ **Warning: `start.sh` may sometimes fail.** If it shows `❌ Backend failed to start` or `Address already in use`, use **Method 2** (manual two-terminal method) below — it is 100% reliable on all platforms. The script does its best to clean up stale processes, but on Linux, the OS occasionally holds onto a port for a few extra seconds after a crash.

**If `start.sh` fails, run this once to fully clear all stale processes, then retry:**
```bash
pkill -f "backend/app.py"; pkill -f "vite"; sleep 3 && bash start.sh
```

**To stop everything:**
Press `Ctrl+C` in the terminal. The script will automatically kill both servers.

---

## 🛡️ Method 2: Manual Two-Terminal Start (Recommended — Works on All Platforms)

This is the most reliable method. Open **two separate terminal windows** in the project folder.

### Quick Reference

| Platform | Terminal 1 (Backend) | Terminal 2 (Frontend) |
|---|---|---|
| **Ubuntu / Linux** | `source venv/bin/activate && python backend/app.py` | `cd frontend && npm run dev` |
| **Mac (Apple Silicon)** | `source venv/bin/activate && python backend/app.py` | `cd frontend && npm run dev` |
| **Windows (CMD)** | `venv\Scripts\activate && python backend\app.py` | `cd frontend && npm run dev` |
| **Windows (PowerShell)** | `venv\Scripts\Activate.ps1; python backend\app.py` | `cd frontend; npm run dev` |

---

### 🐧 Ubuntu / Linux — Step by Step

**Terminal 1 — Backend:**
```bash
cd /path/to/deepthinker
source venv/bin/activate

# Intel Iris Xe iGPU only — skip this on NVIDIA/Mac
export SYCL_DEVICE_FILTER=level_zero
export IPEX_OPTIMIZE_TRANSFORMERS=1

python backend/app.py
```

Wait until you see:
```
🧠 DMA: Detected XX GB RAM → Safety threshold = X.X GB
INFO:     Uvicorn running on http://127.0.0.1:8000
```

**Terminal 2 — Frontend:**
```bash
cd /path/to/deepthinker/frontend
npm run dev
```

---

### 🍎 Mac (Apple Silicon M1/M2/M3/M4) — Step by Step

**Terminal 1 — Backend:**
```bash
cd /path/to/deepthinker
source venv/bin/activate
python backend/app.py
```

**Terminal 2 — Frontend:**
```bash
cd /path/to/deepthinker/frontend
npm run dev
```

---

### 🪟 Windows — Step by Step

**Terminal 1 — Backend (Command Prompt):**
```cmd
cd C:\path\to\deepthinker
venv\Scripts\activate
python backend\app.py
```

**Terminal 1 — Backend (PowerShell):**
```powershell
cd C:\path\to\deepthinker
venv\Scripts\Activate.ps1
python backend\app.py
```

**Terminal 2 — Frontend (both CMD and PowerShell):**
```cmd
cd C:\path\to\deepthinker\frontend
npm run dev
```

---

### Step 3 — Open the UI

Once both terminals show their success messages, open your browser:

```
http://localhost:5173
```

Backend API is at `http://127.0.0.1:8000`

---

## 📥 Downloading Models (First Time Only)

Before running for the first time, download the AI model weights (~18 GB total):

```bash
source venv/bin/activate   # Mac / Linux
# venv\Scripts\activate    # Windows

# Check which models are already downloaded
python backend/downloader.py

# Download all at once
python backend/downloader.py router deepseek_r1 vibethinker opencode qwen_vl

# Or download individually
python backend/downloader.py router          # Phi-3.5 Mini     (~3 GB)
python backend/downloader.py deepseek_r1    # DeepSeek-R1 7B   (~6 GB)
python backend/downloader.py vibethinker    # VibeThinker 1.5B (~1.4 GB)
python backend/downloader.py opencode       # OpenCodeInterpreter 6.7B (~5 GB)
python backend/downloader.py qwen_vl        # Qwen2.5-VL 7B    (~7 GB)
```

---

## 🛠️ Troubleshooting

### ❌ `Address already in use` (Port 8000 or 5173)

A previous server is still running. Kill it first:

**Linux / Mac:**
```bash
pkill -f "backend/app.py"
pkill -f "vite"
sleep 2
```

**Windows (PowerShell):**
```powershell
# Find and kill port 8000
netstat -ano | findstr :8000
taskkill /PID <PID_FROM_ABOVE> /F

# Find and kill port 5173
netstat -ano | findstr :5173
taskkill /PID <PID_FROM_ABOVE> /F
```

---

### ❌ `NetworkError when attempting to fetch resource`

The frontend cannot reach the backend. Check:
1. Is the **backend running** in Terminal 1? Look for `Uvicorn running on http://127.0.0.1:8000`
2. Did the backend **crash**? Check Terminal 1 for error messages
3. In the UI, go to **Settings** and confirm the API URL is `http://127.0.0.1:8000`

---

### ❌ `No module named 'llama_cpp'` or `ModuleNotFoundError`

Virtual environment is not activated or deps not installed:
```bash
source venv/bin/activate   # Mac / Linux
pip install -r requirements.txt
```

---

### ❌ `Aborted (core dumped)` or `CUDA out of memory` on model load

The Dynamic Memory Allocator (DMA) handles this automatically by evicting older models. If it still crashes:
1. Click **"Offload Memory"** in the UI sidebar
2. Retry the prompt — models load one at a time now

---

### ❌ Frontend opens on port 5174 instead of 5173

Port 5173 is still occupied. Kill the stale process:
```bash
pkill -f "vite"    # Linux / Mac
```
Then re-run `npm run dev`. Or just use `http://localhost:5174` — the UI works on any port.

---

## 🧠 System Requirements

| Component | Minimum | Recommended |
|---|---|---|
| **RAM** | 16 GB | 32 GB |
| **GPU VRAM** | 8 GB (NVIDIA/AMD dGPU) | 12 GB+ |
| **Storage** | 25 GB free | 40 GB free |
| **OS** | Ubuntu 22.04 / Win 10 / macOS 13 | Ubuntu 24.04 / Win 11 / macOS 14 |
| **Python** | 3.10 | 3.11 |
| **Node.js** | 18 | 20 |

> **Intel iGPU (Iris Xe / Arc):** The system uses your system RAM as VRAM via the DMA. 32 GB RAM recommended. Always set `SYCL_DEVICE_FILTER=level_zero` before starting.

---

## ✅ What to Expect When Running

Once both servers are up and you submit a prompt, the multi-agent pipeline streams live in the UI:

1. **Phi-3.5 Router** classifies your prompt → `CODING`, `REASONING`, or `SIMPLE`
2. **DeepSeek-R1** drafts a step-by-step logic plan
3. **Reasoning Sandbox** verifies the plan with Python assertions
4. **VibeThinker** writes the code
5. **Execution Sandbox** runs the code in a fully isolated environment
6. **OpenCodeInterpreter** generates an interactive 3D Plotly visualization (if applicable)
7. Final answer streams to the UI with code, output, and visualization
