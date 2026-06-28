# DeepThink AIOS Setup & Hardware Acceleration Guide

Because DeepThink AIOS runs fully local 7B reasoning agents, it requires **hardware acceleration (GPU)**. 

The Python code is OS-agnostic, but PyTorch and `llama.cpp` require different installation commands depending on if you are using an Apple MacBook, a Windows NVIDIA PC, or a Linux Intel machine.

Please follow the instructions for your specific operating system to ensure the models run on your GPU rather than your CPU.

---

## Step 1: System Prerequisites (For Polyglot Sandbox)
DeepThink AIOS can execute code in multiple languages. For this to work, ensure your system has the necessary native compilers installed.

*   **Mac:** Run `xcode-select --install` in terminal (installs `gcc`/`g++`).
*   **Linux:** Run `sudo apt install build-essential openjdk-17-jdk nodejs` (installs C/C++, Java, and Node.js).
*   **Windows:** Install [MinGW](https://www.mingw-w64.org/) for C/C++ and Node.js for Javascript.

*(Note: If a compiler is missing, the AI engine will not crash; it will gracefully fall back to Python execution).*

---

## Step 2: Install Base Python Dependencies
First, install the core dependencies that work on all operating systems:

```bash
# Clone the repository and enter it
git clone https://github.com/Bshdhorrhh/Team_Trenches.git
cd Team_Trenches

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install all package requirements
pip install -r requirements.txt
```

---

## Step 3: Install Hardware Acceleration

Run the specific block below that matches your computer's hardware to enable GPU execution.

### 🍎 Mac (Apple Silicon M1/M2/M3)
Apple uses the "Metal" framework for GPU acceleration.

```bash
# 1. Install Mac-optimized PyTorch
pip install torch torchvision torchaudio

# 2. Install Mac-optimized Llama.cpp (Metal)
CMAKE_ARGS="-DGGML_METAL=on" pip install llama-cpp-python --upgrade --force-reinstall --no-cache-dir
```

### 🪟 Windows / Linux (NVIDIA GPUs)
NVIDIA uses "CUDA" for GPU acceleration. Ensure you have the [CUDA Toolkit](https://developer.nvidia.com/cuda-downloads) installed.

```bash
# 1. Install NVIDIA-optimized PyTorch
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# 2. Install NVIDIA-optimized Llama.cpp (cuBLAS)
set CMAKE_ARGS="-DGGML_CUDA=on"  # On Linux use: export CMAKE_ARGS="-DGGML_CUDA=on"
pip install llama-cpp-python --upgrade --force-reinstall --no-cache-dir
```

### 🐧 Linux (Intel Iris Xe / Arc GPUs)
*This is the default configuration used during the Hackathon development phase.*

```bash
# 1. Install Intel-optimized PyTorch (IPEX)
pip install torch==2.8.0+xpu intel-extension-for-pytorch==2.8.10+xpu --extra-index-url https://download.pytorch.org/whl/xpu

# 2. Install Llama.cpp
pip install llama-cpp-python
```

---

## Step 4: Download Models & Start the System

Once all dependencies are installed, head to **[STARTUP.md](./STARTUP.md)** for:
- How to download the AI model weights (~18 GB)
- How to start the backend and frontend on Ubuntu, Mac, and Windows
- Troubleshooting common errors
