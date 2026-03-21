# GitLens + GitHub 集成设置指南

## 🚀 快速设置

### 1️⃣ VS Code 中配置 GitLens

**已安装的 GitLens 功能：**
- ✅ Blame annotations（行责任追踪）
- ✅ File history（文件历史）
- ✅ Branch explorer（分支浏览）
- ✅ Commit graph（提交图表）

### 2️⃣ 连接 GitHub 账户

**步骤：**
1. VS Code 打开命令面板 → `Ctrl+Shift+P`
2. 搜索 "GitLens" → 选择 "GitLens: Start GitLens"
3. 点击右下角 "Sign in with GitHub"
4. 在浏览器中授权 VS Code 访问你的 GitHub

### 3️⃣ 连接您的 GitHub 仓库

```bash
# 初始化 Git（如果还没有）
cd C:\Users\pc500\Desktop\새 폴더 (2)\playform
git init

# 添加远程仓库
git remote add origin https://github.com/YOUR_USERNAME/playform.git

# 首次推送
git branch -M main
git push -u origin main
```

### 4️⃣ GitLens 常用命令

| 快捷键 | 功能 |
|--------|------|
| `Cmd+Shift+G` (Mac) / `Ctrl+Shift+G` (Windows) | 打开 GitLens |
| `Alt+L` | 查看当前行的 Blame |
| `Alt+H` | 查看文件历史 |
| `Cmd+K Cmd+H` (Mac) / `Ctrl+K Ctrl+H` (Windows) | 显示提交历史 |

### 5️⃣ 常见工作流

#### a) 查看谁修改了某一行
```
1. 在行上右键 → "Open Blame"
2. 显示作者、日期、提交信息
```

#### b) 查看文件变更历史
```
1. 打开命令面板 → "GitLens: Show File History"
2. 查看所有历史版本
```

#### c) 创建分支
```bash
git checkout -b feature/your-feature
git push -u origin feature/your-feature
```

### 6️⃣ Pull Request 工作流（使用 GitLens Launchpad）

**步骤：**
1. 打开 VS Code 侧边栏 → 找到 "Source Control" 图标
2. 选择 "GitLens: Show Launchpad"
3. 查看：
   - 📋 待审核的 PR
   - ⚠️ 有冲突的 PR
   - 🎯 需要你审核的 PR

**创建 PR：**
```bash
# 1. 创建本地分支
git checkout -b feature/new-feature

# 2. 提交更改
git add .
git commit -m "feat: add new feature"

# 3. 推送到 GitHub
git push -u origin feature/new-feature

# 4. 在 GitHub 网站上创建 PR
# 或在 VS Code 中使用 GitLens → "Create Pull Request"
```

---

## 📌 Playform 项目 Git 配置

### 项目结构
``` 
./
├── .git/                 # Git 仓库
├── apps/
│   └── core/
│       ├── backend/      # FastAPI 后端
│       └── frontend/     # React 前端
├── .github/
│   └── workflows/        # GitHub Actions（CI/CD）
└── .gitignore            # 忽略文件
```

### 已忽略的文件（不会上传到 GitHub）
- `.env` - 环保变量（包含 API 密钥）
- `node_modules/` - npm 依赖
- `.venv/` - Python 虚拟环境
- `*.db` - SQLite 数据库
- `__pycache__/` - Python 缓存

---

## 🔐 安全提醒

⚠️ **永远不要提交到 GitHub：**
- `.env` 文件（包含 API 密钥和密码）
- `service-account-key.json`（Firebase 凭证）
- 任何个人或敏感信息

✅ **安全的做法：**
1. 使用 `.env.example` 作为模板，提交到 GitHub
2. 本地创建 `.env`，添加你的实际密钥
3. `.gitignore` 会自动忽略 `.env`

---

## 🚀 推荐的进一步步骤

1. **设置 GitHub Actions（CI/CD）**
   - 自动运行测试
   - 自动部署

2. **配置 Branch Protection Rules**
   - 要求 PR 审核
   - 自动检查测试通过

3. **配置 Issues 和 Discussions**
   - 跟踪功能需求
   - 报告 Bug

---

## 📚 更多资源

- [GitLens 官方文档](https://www.gitkraken.com/gitlens)
- [GitHub CLI 文档](https://cli.github.com/)
- [Git 官方教程](https://git-scm.com/doc)

---

设置完成时间：2026-02-25
