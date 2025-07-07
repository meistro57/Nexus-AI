#!/usr/bin/env bash
set -e

# Update repository
if git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
  echo "Updating repository..."
  git pull --ff-only
fi

# Start backend
pushd backend > /dev/null
python3 -m venv .venv >/dev/null 2>&1 || true
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload &
BACKEND_PID=$!
popd > /dev/null

# Start frontend
pushd frontend > /dev/null
npm install
npm run dev &
FRONTEND_PID=$!
popd > /dev/null

echo "Backend running with PID $BACKEND_PID"
echo "Frontend running with PID $FRONTEND_PID"

trap "echo Stopping...; kill $BACKEND_PID $FRONTEND_PID" INT TERM

wait $BACKEND_PID $FRONTEND_PID
