# 🧠 DeepThinker Multi-Agent Hub

> **India Agentic AI Open Hackathon 2026 — Team Trenches**

A production-grade, fully local multi-agent AI system that runs **five heavyweight LLMs simultaneously** on consumer hardware — including Intel Iris Xe integrated GPUs. DeepThinker routes every query through a dynamic pipeline of specialized agents that reason, verify, code, fix, and visualize — all without a single API call to the cloud.

---

## ✨ What Makes This Different

Most "local AI" projects run a single model and call it agentic. DeepThinker runs an **orchestrated pipeline of 5 models** with a loop-based Actor-Critic architecture, a live code execution sandbox, and a 3D visualization engine — all on a 32 GB laptop.

| Feature | DeepThinker | Typical Local LLM App |
|---|---|---|
| Number of models | 5 (routed) | 1 |
| Code execution | ✅ Isolated polyglot sandbox | ❌ |
| Self-correction | ✅ Reflexion + Nuclear Reset | ❌ |
| 3D Visualization | ✅ Live Plotly rendering | ❌ |
| Memory / RAG | ✅ ChromaDB + SQLite | ❌ |
| Hardware | Intel iGPU / NVIDIA / Mac M-series | Usually NVIDIA only |
| Cloud dependency | ❌ 100% local | Often cloud-backed |

---

## 🤖 The Agent Pipeline

```
User Prompt
    │
    ▼
┌─────────────────────────────────┐
│  Phi-3.5-Mini (Master Router)  │  ← Classifies: SIMPLE / CODING / REASONING
└───────────────┬─────────────────┘
                │
    ┌───────────┼───────────┐
    ▼           ▼           ▼
 SIMPLE      CODING     REASONING
    │           │           │
    │    ┌──────┴──────┐    └──────────────┐
    │    ▼             ▼                   ▼
    │ DeepSeek-R1  DeepSeek-R1       DeepSeek-R1
    │ (Logic Plan) (Logic Plan)      (Draft Answer)
    │    │             │                   │
    │    ▼             ▼                   ▼
    │ Reasoning    Reasoning          Reasoning
    │ Sandbox      Sandbox ──────► Playground
    │ (Verify)     (Verify)        (Verify via Python)
    │    │             │                   │
    │    ▼             ▼                   ▼
    │ VibeThinker  VibeThinker        VibeThinker
    │ (Write Code) (Fix Logic)       (Critique & Refine)
    │    │             │                   │
    │    ▼             ▼                   ▼
    │ Execution    Execution         3D Gate Check
    │ Sandbox      Sandbox               │
    │    │         (Reflexion             ▼
    │    │          Loop ×3)    OpenCodeInterpreter
    │    │             │        (Plotly 3D Chart)
    │    ▼             ▼                   │
    └────┴─────────────┴───────────────────┘
                       │
                       ▼
              Streamed Response
          (Answer + Code + 3D Chart)
```

---

## 🧩 The Five Agents

| Agent | Model | Role | Size |
|---|---|---|---|
| **Master Router** | Phi-3.5-Mini Q6_K | Classifies intent, prompt compression, 3D gate | ~3 GB |
| **Reasoning Engine** | DeepSeek-R1-Distill-Qwen-7B Q6_K | Chain-of-thought logic, math proofs, deep analysis | ~6 GB |
| **Omni AGI Core** | VibeThinker 1.5B Q6_K | Code writing, Reflexion self-fix, Actor-Critic debate | ~1.4 GB |
| **3D Visualization** | OpenCodeInterpreter-DS 6.7B Q6_K | Plotly 3D chart generation, code execution | ~5 GB |
| **Vision Parser** | Qwen2.5-VL 7B Q6_K_XL | Multimodal image/document OCR and analysis | ~7 GB |

---

## 🛡️ Core Systems

### Dynamic Memory Allocator (DMA)
The DMA is a custom memory manager built specifically for running multiple large models on consumer hardware. It:
- Auto-detects available RAM and sets a safety threshold (25% of total)
- Uses **LRU eviction** — evicts the least recently used model when memory is tight
- Has an **iGPU Unified Memory Guard** that prevents glibc heap corruption when multiple 7B models coexist on Intel iGPUs
- Supports **lazy loading** — models load only when the pipeline actually needs them, not all at startup

### Polyglot Execution Sandbox
A three-layer isolated code execution environment:
- **Layer 1:** Process isolation (code runs in a subprocess, can't crash the server)
- **Layer 2:** Restricted builtins (custom `__import__` whitelist, no `open`/`exec`/`os`)  
- **Layer 3:** Linux resource limits (1 GB RAM cap, 120s CPU limit, 50 child process limit)
- Auto-detects and executes **Python, C, C++, Java, JavaScript, and Bash**
- Falls back to unrestricted mode if the restricted sandbox blocks a legitimate library

### Reflexion Self-Fix Loop
When generated code fails, the system doesn't just report the error — it fixes it:
1. VibeThinker attempts a shallow fix
2. If that fails, deep escalation with a stronger prompt
3. If that fails, **Nuclear Reset**: extract lessons from all failures and rewrite from scratch
4. Up to **3 complete reset cycles** before returning best-effort output

### Long-Term Memory (RAG)
- **ChromaDB** vector database for semantic similarity search
- **SQLite** fallback with keyword-based search and cosine similarity
- Stores compact solution summaries (not raw code dumps) to avoid context bloat
- Stores mistake-fix patterns to prevent regression on similar future prompts

---

## 🖥️ Hardware Compatibility

| Hardware | Status | Notes |
|---|---|---|
| **Intel Iris Xe iGPU** | ✅ Full support | Uses system RAM as VRAM via Level Zero API |
| **Intel Arc dGPU** | ✅ Full support | Same SYCL/Level Zero path |
| **NVIDIA (CUDA)** | ✅ Full support | cuBLAS acceleration via llama.cpp |
| **AMD (ROCm)** | ✅ Full support | ROCm path via PyTorch + llama.cpp |
| **Apple Silicon (M1-M4)** | ✅ Full support | Metal backend, no crashes |
| **CPU only** | ✅ Works | Slow but functional (switch to `device_mode: cpu` in settings) |

### Intel Iris Xe — Special Notes
Running 7B+ models on iGPUs is notoriously unstable. These fixes are baked into the codebase:

- **Error 45 (`UR_RESULT_ERROR_INVALID_ARGUMENT`)**: Fixed via `SYCL_PI_LEVEL_ZERO_USE_IMMEDIATE_COMMANDLISTS=1` in `app.py`
- **`corrupted size vs. prev_size` heap crash**: Fixed via the DMA iGPU Guard which prevents simultaneous large allocations
- **Float16 kernel failures**: Models fall back to `float32` on XPU with IPEX optimization applied automatically

---

## 🚀 Quick Start

### 1. Clone & Install
```bash
git clone https://github.com/Scorpio-4488/Team_Trenches.git
cd Team_Trenches

python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Install frontend deps
cd frontend && npm install && cd ..
```

### 2. Install GPU Acceleration (pick your hardware)

**Mac (Apple Silicon):**
```bash
pip install torch torchvision torchaudio
CMAKE_ARGS="-DGGML_METAL=on" pip install llama-cpp-python --upgrade --force-reinstall --no-cache-dir
```

**NVIDIA GPU:**
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
export CMAKE_ARGS="-DGGML_CUDA=on"
pip install llama-cpp-python --upgrade --force-reinstall --no-cache-dir
```

**Intel Iris Xe / Arc (Linux):**
```bash
pip install torch==2.8.0+xpu intel-extension-for-pytorch==2.8.10+xpu --extra-index-url https://download.pytorch.org/whl/xpu
pip install llama-cpp-python
```

> See [README_SETUP.md](./README_SETUP.md) for the complete hardware setup guide.

### 3. Download Models (~18 GB)
```bash
python backend/downloader.py
```

### 4. Run

**Option A — One command (Linux):**
```bash
bash start.sh
```

**Option B — Manual two terminals (all platforms):**
```bash
# Terminal 1 — Backend
source venv/bin/activate
python backend/app.py

# Terminal 2 — Frontend
cd frontend && npm run dev
```

> See [STARTUP.md](./STARTUP.md) for the full cross-platform startup guide and troubleshooting.

Open **`http://localhost:5173`** in your browser.

---

## 📁 Project Structure

```
Team_Trenches/
├── backend/
│   ├── app.py            # FastAPI server, all REST endpoints, SSE streaming
│   ├── orchestrator.py   # Core multi-agent pipeline, DMA, Reflexion loops
│   ├── sandbox.py        # Polyglot code execution sandbox (Python/C/C++/Java/JS/Bash)
│   ├── memory.py         # Long-term RAG memory (ChromaDB + SQLite)
│   ├── search.py         # Web search (Google → SearXNG → DuckDuckGo fallback)
│   └── downloader.py     # Model downloader with retry logic and progress bar
├── frontend/
│   └── src/
│       └── App.jsx       # React UI with live streaming, 3D Plotly rendering, agent timeline
├── models/               # Downloaded GGUF weights (git-ignored, ~18 GB)
├── start.sh              # One-command Linux launcher
├── STARTUP.md            # Cross-platform startup guide
├── README_SETUP.md       # Hardware acceleration installation guide
└── requirements.txt      # Python dependencies
```

---

## 🔌 API Reference

| Endpoint | Method | Description |
|---|---|---|
| `/api/chat` | `POST` | Main chat endpoint, streams SSE status + final response |
| `/api/status` | `GET` | System health, model status, RAM/CPU usage |
| `/api/download/{model_key}` | `POST` | Trigger background model download |
| `/api/cancel` | `POST` | Stop active generation (models stay loaded) |
| `/api/offload` | `POST` | Unload all models from RAM/VRAM |
| `/api/settings` | `POST` | Update context length, temperature, GPU layers |
| `/api/memory/count` | `GET` | Number of stored long-term memories |
| `/api/memory/clear` | `POST` | Reset the vector database |

---

## 🧪 Example Prompts to Try

**3D Physics Simulation:**
> *Simulate the orbital mechanics of a binary star system. Give me the mathematical explanation, and then generate an interactive 3D visualization showing the orbital paths of the two stars.*

**Deep Reasoning + Verification:**
> *Prove that the sum of the first N natural numbers is N(N+1)/2. Verify it computationally for N=100.*

**Reflexion Loop Test:**
> *Write a Python implementation of a Red-Black Tree with insert, delete, and search operations. Include test cases.*

**Vision + Coding (upload an image):**
> *Analyze this circuit diagram and write the Python simulation for it.*

---

## 👥 Team

**Team Trenches** — India Agentic AI Open Hackathon 2026

---

## 📄 License

MIT License — see [LICENSE](./LICENSE) for details.
