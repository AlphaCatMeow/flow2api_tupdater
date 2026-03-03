# Flow2API Token Updater v3.0

轻量版 Token 自动更新工具，通过 Playwright 持久化 Profile 管理 Google Labs 登录状态，并用 Headless 模式定时刷新 Token。

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/genz27/flow2api_tupdater&project-name=flow2api-token-updater&repository-name=flow2api_tupdater&env=ADMIN_PASSWORD,API_KEY,FLOW2API_URL,CONNECTION_TOKEN)

## 特性

- 🪶 轻量化：VNC/Xvfb/noVNC 按需启动（仅登录时运行），降低常驻内存占用
- 🔄 自动刷新：定时刷新 Token 并推送到 Flow2API
- 👥 多 Profile：支持管理多个账号（Profile 级隔离）
- 🌐 代理支持：每个 Profile 可配置独立代理
- 🖥️ 可视化登录：需要时开启 VNC 登录，关闭浏览器后自动停止以省内存

## 一键部署

### Vercel

点击上方按钮即可导入仓库到 Vercel。

建议在 Vercel 项目中至少配置以下环境变量：

- `ADMIN_PASSWORD`
- `API_KEY`
- `FLOW2API_URL`
- `CONNECTION_TOKEN`

Vercel 运行时限制说明：

- 默认关闭 VNC 登录入口，浏览器可视化登录不适用于 Vercel
- 不启动内置定时任务；如需自动同步，请改用 Vercel Cron 或外部 Cron 请求接口
- 本地数据库和 Profile 数据默认写入 `/tmp`，实例重启后不会持久保留

如果你需要长期保存登录状态、使用 Playwright 浏览器登录或依赖定时任务，仍然建议使用下面的 Docker 方式部署。

## 快速开始

```bash
# 克隆仓库
git clone https://github.com/genz27/flow2api_tupdater.git
cd flow2api_tupdater

# 配置环境变量
cp .env.example .env
# 编辑 .env 设置 ADMIN_PASSWORD 等

# 启动（或更新后重建）
docker compose up -d --build

```

访问 http://localhost:8002 进入管理界面。

## 使用流程

1. 创建 Profile
2. 点击「登录」→ 打开 VNC 完成 Google 登录
3. 点击「关闭浏览器」保存状态（VNC 会自动停止以节省内存）
4. 配置 Flow2API 连接信息（`FLOW2API_URL` / `CONNECTION_TOKEN`）
5. 开始自动同步

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| ADMIN_PASSWORD | 管理界面密码 | admin123 |
| API_KEY | 外部 API 密钥 | - |
| FLOW2API_URL | Flow2API 地址 | http://host.docker.internal:8000 |
| CONNECTION_TOKEN | Flow2API 连接 Token | - |
| REFRESH_INTERVAL | 刷新间隔(分钟) | 60 |
| ENABLE_VNC | 是否启用 VNC 登录入口(1/0) | 1 |
| VNC_PASSWORD | VNC 密码（开启 VNC 时使用） | flow2api |
| DB_PATH | SQLite 数据库文件路径 | /app/data/profiles.db |
| PROFILES_DIR | 浏览器 Profile 存储目录 | /app/profiles |
| CONFIG_FILE | 持久化配置文件路径 | /app/data/config.json |

## API

### 外部 API (需要 X-API-Key)

- `GET /v1/profiles` - 列出所有 Profile
- `GET /v1/profiles/{id}/token` - 获取 Token
- `POST /v1/profiles/{id}/sync` - 同步到 Flow2API

## 从 v2.0 升级

v3.1 使用持久化 Profile 登录（按需启停 VNC 以降低内存）：

1. 备份 `data/` 目录
2. 拉取新版本
3. 重新构建镜像
4. 如需重新授权：进入管理界面逐个 Profile 点击「登录」完成 Google 登录

## License

MIT
