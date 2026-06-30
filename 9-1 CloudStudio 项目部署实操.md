# 9\-1 CloudStudio 项目部署实操

实训项目开发开发完毕后，需要部署到远程环境，可随时访问。

项目部署有多种方式，如果有云服务器的话，部署就比较方便。如果没有的话，可以使用 CloudStudio来进行项目部署。



## 一、准备工作

1. 注册 CloudStudio  

访问地址：https://cloudstudio\.net/， 注册送50机时，（CPU 4核8G）。 

可支持python等语言环境。



2. 在项目中配置支持CloudStudio的一键启动脚本

几个调整文件的内容，见[调整文件\.md](https://hypersmart.feishu.cn/wiki/EsGBwrT0zivdUDkr7dWchMDEngP)，具体如下：

（1）新增`start.sh`一键启动脚本，放在根目录:   【下载链接：[start\.sh](https://hypersmart.feishu.cn/wiki/GVL9wxJ3ZiFYw7kZy9rcSog1n9b)】

```Bash
#!/usr/bin/env bash
# ==========================================================
# CloudStudio 全栈沙箱 — 一键启动脚本
# 自动安装依赖并同时启动前后端服务
# ==========================================================
set -e

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

APP_NAME="📒 个人记账本"

echo -e "${CYAN}========================================${NC}"
echo -e "${CYAN}  ${APP_NAME} — CloudStudio 全栈启动 ${NC}"
echo -e "${CYAN}========================================${NC}"
echo ""

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$PROJECT_DIR/backend"
FRONTEND_DIR="$PROJECT_DIR/frontend"

# --------------- 后端 ---------------
echo -e "${YELLOW}[1/4] 安装后端依赖...${NC}"
cd "$BACKEND_DIR"
pip install -r requirements.txt -q 2>/dev/null || pip install -r requirements.txt

echo -e "${YELLOW}[2/4] 启动后端服务 (端口 8000)...${NC}"
cd "$BACKEND_DIR"
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
echo -e "${GREEN}  后端 PID: $BACKEND_PID${NC}"

# 等待后端就绪
sleep 2
# --------------- 种子数据 ---------------
echo -e "${YELLOW}[2.5/4] 初始化预设分类数据...${NC}"
cd "$BACKEND_DIR"
python seed.py

# --------------- 前端 ---------------
echo -e "${YELLOW}[3/4] 安装前端依赖...${NC}"
cd "$FRONTEND_DIR"
if [ ! -d "node_modules" ]; then
  npm install
fi

echo -e "${YELLOW}[4/4] 启动前端开发服务器 (端口 3000)...${NC}"
cd "$FRONTEND_DIR"
npx vite --host 0.0.0.0 --port 3000 &
FRONTEND_PID=$!
echo -e "${GREEN}  前端 PID: $FRONTEND_PID${NC}"

# --------------- 完成 ---------------
echo ""
echo -e "${CYAN}========================================${NC}"
echo -e "${GREEN}  ✅ ${APP_NAME} 已启动！${NC}"
echo -e "${CYAN}========================================${NC}"
echo ""
echo -e "  📡 前端地址:  ${GREEN}http://localhost:3000${NC}"
echo -e "  📡 后端地址:  ${GREEN}http://localhost:8000${NC}"
echo -e "  📖 API 文档:  ${GREEN}http://localhost:8000/docs${NC}"
echo ""
echo -e "  ${YELLOW}💡 CloudStudio 会自动检测打开的端口，${NC}"
echo -e "  ${YELLOW}   生成可公开访问的预览链接。${NC}"
echo ""
echo -e "  ${YELLOW}按 Ctrl+C 停止所有服务${NC}"
echo ""

# 捕获退出信号，清理子进程
cleanup() {
  echo ""
  echo -e "${YELLOW}正在停止服务...${NC}"
  kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true
  wait $BACKEND_PID $FRONTEND_PID 2>/dev/null || true
  echo -e "${GREEN}服务已停止。${NC}"
  exit 0
}
trap cleanup SIGINT SIGTERM

# 保持前台运行
wait

```

（2）修改 vite\.config\.ts 前端配置，放在 frontend/ 【下载链接：  [vite\.config\.ts](https://hypersmart.feishu.cn/wiki/Lne7wGIHDiT4zHktuzpcicbinvc)】

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=MjUwYWUxMGU3MDA4OTZjYjY0OWFhYjRhMmQ4MmE1YzJfN2FkYzljMzIzZmQ4MjBjYzBkZWE3YmJlZDAxZjkxYzRfSUQ6NzY1MjI0MDAwNzc3MjE0NjY1Nl8xNzgyODA0NzAzOjE3ODI4OTExMDNfVjM)

（3）新增空白\.env文件， Vite 环境变量模板，放在 frontend/ 【下载链接：  [\.env](https://hypersmart.feishu.cn/wiki/RGV1war40igIbFk6SBKcV0Dun6c)】

空白文件

（4）修改 request\.ts 请求代理类，放在 frontend/src/utils/ 【下载链接： [request\.ts](https://hypersmart.feishu.cn/wiki/QEmlwlETDiwcJlk26vQctJEUnIc)】

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=MDk2YWEyODZhM2I3OWJkZTFkZGM3Zjc4ZjIzMDBlMzJfOWNjNTQ3Y2U3YjFkNGNiMjIxMGVlODA0OGQ4ZDBmOWNfSUQ6NzY1MjI0MDY0NTM3NzI0ODE5Nl8xNzgyODA0NzAzOjE3ODI4OTExMDNfVjM)



3. 代码推送到gitee



## 二、CloudStudio部署

1. 打开 cloudstudio\.net → 个人中心 → 创建应用 → 从 Git 仓库导入

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=Zjk3ZWUyMjQ2MGFjYjc1MjZjNzNkYzFkY2FjNmM3ZjlfYmVmNjU4ZTBlNWEwM2ZiMDRjOTQwNmRiNjNlZjcyOTVfSUQ6NzY1MjIyMjY5OTA1MzQxOTQ2N18xNzgyODA0NzAzOjE3ODI4OTExMDNfVjM)

选择你的仓库，例如：tanclaw/grjzb



2. 等待环境初始化完成后，打开CloudStudio 的终端界面，输入 sh start\.sh 即可。

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=MGIwZTc2Mzc0NWMxN2RiYzQ3ZWZiYzA0NDQxOWUwZmNfMTJmZjEwYTA0YjA4ZjAxOTVjN2RkNzg1ZjVjMTc4M2NfSUQ6NzY1MjI0MTgwNjI5Nzg3NzQ0MF8xNzgyODA0NzAzOjE3ODI4OTExMDNfVjM)

启动完成后，前后端全栈运行中。

运行后 cloudstudio 会自动在自带的浏览器中打开 前端页面。复制URL链接即可外部访问。如下面地址：

https://b773e476a5b64696b709a1303cea3952\-\-3000\.ap\-shanghai2\.cloudstudio\.club/



## 🌐 CloudStudio部署架构说明

CloudStudio 部署模式下，前端通过 Vite proxy 转发 API 请求：

```Plain Text
浏览器 ──► Vite Dev Server (端口 3000)
                  │
                  ├── 静态资源 ──► 直接返回
                  │
                  └── /api/* ────► proxy ──► FastAPI (端口 8000)
                                                    │
                                                    └── SQLite
```

这样浏览器只访问一个端口（3000），没有跨域问题。



