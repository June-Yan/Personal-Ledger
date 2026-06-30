#!/bin/sh
# ==========================================================
# CloudStudio 全栈沙箱 — 一键启动脚本 (POSIX sh 兼容)
# ==========================================================

APP_NAME="个人记账本"

echo "========================================"
echo "  ${APP_NAME} — CloudStudio 全栈启动"
echo "========================================"
echo ""

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="${PROJECT_DIR}/backend"
FRONTEND_DIR="${PROJECT_DIR}/frontend"

# --------------- 后端 ---------------
echo "[1/4] 安装后端依赖..."
cd "${BACKEND_DIR}"
pip install -r requirements.txt

echo "[2/4] 启动后端服务 (端口 8000)..."
cd "${BACKEND_DIR}"
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload > backend.log 2>&1 &
BACKEND_PID=$!
echo "  后端 PID: ${BACKEND_PID}"

# 等待后端就绪
echo "  等待后端就绪..."
i=0
while [ $i -lt 30 ]; do
  if curl -s http://localhost:8000/ > /dev/null 2>&1; then
    echo "  后端已就绪！"
    break
  fi
  i=$((i + 1))
  sleep 1
done
if [ $i -eq 30 ]; then
  echo "  后端启动超时，日志:"
  cat backend.log
  exit 1
fi

# --------------- 种子数据 ---------------
echo "[2.5/4] 初始化数据库..."
cd "${BACKEND_DIR}"
python seed.py || echo "  数据库已存在，跳过"

# --------------- 前端 ---------------
echo "[3/4] 安装前端依赖..."
cd "${FRONTEND_DIR}"
if [ ! -d "node_modules" ]; then
  npm install
fi

echo "[4/4] 启动前端开发服务器 (端口 3000)..."
cd "${FRONTEND_DIR}"
npx vite --host 0.0.0.0 --port 3000 > frontend.log 2>&1 &
FRONTEND_PID=$!
echo "  前端 PID: ${FRONTEND_PID}"

# 等待前端就绪
echo "  等待前端就绪..."
i=0
while [ $i -lt 30 ]; do
  if curl -s http://localhost:3000/ > /dev/null 2>&1; then
    echo "  前端已就绪！"
    break
  fi
  i=$((i + 1))
  sleep 1
done
if [ $i -eq 30 ]; then
  echo "  前端启动超时，日志:"
  cat frontend.log
  exit 1
fi

# --------------- 完成 ---------------
echo ""
echo "========================================"
echo "  ${APP_NAME} 已启动！"
echo "========================================"
echo ""
echo "  前端地址: http://localhost:3000"
echo "  后端地址: http://localhost:8000"
echo "  API 文档: http://localhost:8000/docs"
echo ""
echo "  CloudStudio 会自动检测端口"
echo "  生成可公开访问的预览链接"
echo ""
echo "  按 Ctrl+C 停止所有服务"
echo ""

# 捕获退出信号
cleanup() {
  echo ""
  echo "正在停止服务..."
  kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
  wait $BACKEND_PID $FRONTEND_PID 2>/dev/null
  echo "服务已停止。"
  exit 0
}
trap cleanup 2 15

# 保持前台运行
wait
