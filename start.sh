#!/bin/bash

# Terminate ALL child processes on Ctrl+C or exit
trap "echo ''; echo 'Shutting down...'; pkill -f 'backend/app.py'; pkill -f 'vite'; exit 0" SIGINT SIGTERM EXIT

echo "============================================="
echo "   Starting DeepThinker Multi-Agent Hub...   "
echo "============================================="

# Intel Iris Xe iGPU environment
export SYCL_DEVICE_FILTER=level_zero
export IPEX_OPTIMIZE_TRANSFORMERS=1

# Source Intel oneAPI compiler if available
if [ -f "/opt/intel/oneapi/compiler/latest/env/vars.sh" ]; then
    echo "Sourcing Intel oneAPI Compiler environment variables..."
    source /opt/intel/oneapi/compiler/latest/env/vars.sh >/dev/null 2>&1
elif [ -f "/opt/intel/oneapi/compiler/2026.0/env/vars.sh" ]; then
    source /opt/intel/oneapi/compiler/2026.0/env/vars.sh >/dev/null 2>&1
fi

if [ -f "/opt/intel/oneapi/mkl/2026.0/env/vars.sh" ]; then
    echo "Sourcing Intel MKL environment variables..."
    source /opt/intel/oneapi/mkl/2026.0/env/vars.sh >/dev/null 2>&1
fi

# ── Clean up any stale processes from previous runs ──────────────────────────
echo "Cleaning up any previous server instances..."
pkill -f "backend/app.py" 2>/dev/null
pkill -f "vite" 2>/dev/null
# Give the OS 2 seconds to fully release the ports
sleep 2

# ── Start Backend ─────────────────────────────────────────────────────────────
echo "Launching FastAPI Backend..."
venv/bin/python backend/app.py &
BACKEND_PID=$!

# Wait and verify the backend actually bound to the port
echo "Waiting for backend to initialize..."
for i in {1..10}; do
    sleep 1
    if ss -tlnp 2>/dev/null | grep -q ':8000'; then
        echo "✅ Backend is up on http://127.0.0.1:8000"
        break
    fi
    if [ $i -eq 10 ]; then
        echo "❌ Backend failed to start. Check the error above."
        exit 1
    fi
done

# ── Start Frontend ────────────────────────────────────────────────────────────
echo "Launching React/Vite Frontend..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

sleep 2

echo "============================================="
echo "🟢 Both servers are running!"
echo "👉 Web UI URL:     http://localhost:5173"
echo "👉 Backend API:    http://127.0.0.1:8000"
echo "Press Ctrl+C to stop both servers."
echo "============================================="

# Keep the script alive until Ctrl+C
wait
