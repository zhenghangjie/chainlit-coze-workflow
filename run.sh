#!/bin/bash

# 切换到 backend 目录并启动 uvicorn
cd backend
echo "Starting uvicorn..."

python3 -m uvicorn app:app --port 8001 --reload &
uvicorn_pid=$!

# 切换回上级目录
cd ..

# 切换到 frontend 目录并启动 npm
cd frontend
echo "Starting npm dev server..."
npm run dev &
npm_pid=$!

# 等待两个进程结束
wait $uvicorn_pid
wait $npm_pid