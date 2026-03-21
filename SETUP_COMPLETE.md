# Playform - MCP & API 设置完成 ✅

## ✅ 已完成的配置

### 1. Python 环境 ✓
- ✅ 虚拟环境：`apps/core/backend/.venv`
- ✅ 所有依赖已安装（fastapi, pydantic, sqlmodel, firebase-admin, mcp 等）
- ✅ VS Code Pylance 配置正确
- ✅ 无导入错误

### 2. MCP (Model Context Protocol) ✓
- ✅ Playform MCP Server：`mcp_server.py`
- ✅ Notion MCP Server：已配置
- ✅ Claude Code 配置：`~/.claude/settings.json`

### 3. API 密钥 ✓
- ✅ Google API Key：已配置在 `.env` 文件中
- ✅ Notion API：已配置（請查閱 .env 檔案）
- ✅ 环境变量自动加载（python-dotenv）

## 🚀 启动应用

### Backend (FastAPI)
```powershell
cd apps\core\backend
.\\.venv\Scripts\activate
uvicorn main:app --reload --port 8000
```

### Frontend (React + Vite)
```powershell
cd apps\core\frontend
npm install  # 首次运行
npm run dev  # 启动开发服务器 (http://localhost:5173)
```

### MCP Server (用于 Claude Code)
```powershell
python mcp_server.py
```

## 🔧 环境变量

环境变量存储在 `.env` 文件中（已在 .gitignore 中）：

```env
GOOGLE_API_KEY=your-google-api-key
PLAYFORM_API=http://127.0.0.1:8000
PLAYFORM_SECRET=your-secret-key
```

## 🔐 安全提醒

⚠️ **重要**：您的 Google API Key 已暴露在聊天记录中！

请立即：
1. 前往 [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
2. **删除或重新生成**该密钥
3. 更新本地 `.env` 文件
4. 永远不要在公共场合分享 API 密钥

## 📝 使用 Claude Code 与 MCP

在 VS Code 中：
1. 按 `Cmd+Shift+P` (Mac) 或 `Ctrl+Shift+P` (Windows)
2. 输入 "Claude Code: Open"
3. 现在 Claude 可以访问：
   - Playform API（通过 MCP）
   - Notion（通过 MCP）

尝试询问 Claude：
```
@playform list all games
@notion 创建一个新页面
```

## 🎯 下一步

- [ ] 测试 Backend API
- [ ] 测试 Frontend
- [ ] 配置 Firebase Firestore（可选）
- [ ] 部署到云端（可选）

---

配置完成时间：2026-02-25
