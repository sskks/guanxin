## 观心（Guān Xīn）项目架构文档

> 最后更新：2026-06-22

---

### 1. 当前架构结论

观心当前仍是一个可运行的单文件 SPA，真实线上入口是根目录 `index.html`。

为了支持后续 UI 升级、功能迭代和商业化，本项目已经开始建立前后端分层骨架：

- `apps/web`：未来前端应用
- `apps/api`：未来后端服务
- `packages/design-system`：设计系统
- `packages/domain`：易学算法与业务纯逻辑
- `packages/content`：内容、术语、prompt 与运营文本

重要说明：这些新目录目前是架构骨架和迁移目标，**尚未替代当前运行入口**。任何开发都必须保证根目录 `index.html` 继续可运行。

---

### 2. 当前技术栈

#### 前端

- HTML5
- CSS3
- Vanilla JavaScript ES6+
- Google Fonts CDN：Noto Serif SC + Ma Shan Zheng
- IndexedDB：占卦记录
- localStorage：用户设置、出生信息、签到状态

#### 后端

- `server.py`
- Python `http.server`
- 本地静态文件服务
- DashScope / Qwen AI 代理

#### 部署

- Cloudflare Pages：主
- GitHub Pages：备
- 本地开发：`python server.py`

当前不使用：

- npm
- TypeScript
- React / Vue / Angular
- Vite / Webpack
- 数据库
- 账号系统

---

### 3. 目录结构

```text
Cculture/
├── index.html                  # 当前真实运行入口
├── prototype.html              # 原型/同步副本
├── server.py                   # 当前本地开发服务器 + AI API 代理
├── PRODUCT.md                  # 产品级上下文
├── DESIGN.md                   # 设计系统上下文
├── README.md
├── AGENTS.md
│
├── apps/
│   ├── web/                    # 未来前端应用目录
│   └── api/                    # 未来后端服务目录
│
├── packages/
│   ├── design-system/          # 设计 token 与组件样式
│   ├── domain/                 # 起卦、命宫、八宅等纯逻辑
│   └── content/                # 解释文本、术语、prompt、运营内容
│
├── docs/
│   ├── PRD.md
│   ├── PRODUCT_STRATEGY.md
│   ├── DEVELOPMENT_PLAN.md
│   ├── PROJECT_STATE.md
│   ├── ARCHITECTURE.md
│   ├── DEVELOPMENT.md
│   ├── COMMERCIAL_ARCHITECTURE.md
│   └── UI_UX_UPGRADE_PLAN.md
│
├── css/                        # 早期预留目录，暂未接入运行入口
├── js/                         # 早期预留目录，暂未接入运行入口
├── data/                       # 早期预留目录，暂未接入运行入口
├── patches/                    # 历史补丁与整理目录
└── *.py                        # 历史补丁脚本与本地服务
```

---

### 4. 当前运行入口：index.html

`index.html` 是当前唯一完整应用文件，包含：

- CSS 设计令牌与全部样式
- 11 个 screen 页面容器
- 六十四卦、命宫、八宅等数据表
- 起卦、命宫、八宅、主题分类等逻辑
- IndexedDB 与 localStorage 存储逻辑
- AI 解读请求逻辑
- 弹窗、设置、新手引导与分享逻辑

当前导航由 `goTo(screenId)` 控制，通过 `.screen.active` 切换页面可见性。

---

### 5. 目标分层

#### apps/web

未来承接：

- 页面结构
- 路由与导航
- 状态管理
- UI 组件装配
- 与 API 通信

当前只作为迁移目标，不参与运行。

#### apps/api

未来承接：

- AI 代理
- 用户系统
- 记录同步
- 会员权益
- 支付 Webhook
- 内容管理

当前 `server.py` 仍是实际后端。

#### packages/design-system

未来承接：

- 色彩 token
- 字体 token
- 间距 token
- 动效 token
- 通用组件样式

首批迁移目标是 `index.html` 的 `:root` token。

#### packages/domain

未来承接与 UI 无关的纯逻辑：

- 数字起卦
- 梅花易数起卦
- 命宫计算
- 八宅计算
- 主题分类
- 七日回看规则

要求不访问 DOM、不读写 localStorage / IndexedDB。

#### packages/content

未来承接：

- 卦辞白话解释
- 象辞解释
- 爻辞解释
- 新手术语解释
- 今日一问
- 节气专题
- AI prompt 模板

---

### 6. 数据模型

#### IndexedDB：占卦记录

数据库：`GuanXinDivination`

对象存储：`records`

主键：`date`

核心字段：

- `date`
- `question`
- `hexName`
- `hexIndex`
- `upperTri`
- `lowerTri`
- `changingYao`
- `theme`
- `favorite`
- `reviewedAt`
- `summary`
- `method`

#### localStorage

当前键：

- `guanxin_birth`
- `guanxin_onboarded`
- `guanxin_checkins`
- `guanxin_apikey`
- `guanxin_pending_nav`

商业化后，应将跨设备数据迁移到服务端，本地存储仅作为离线和未登录兜底。

---

### 7. API 边界

当前已存在：

- `POST /api/ai-interpret`

未来建议演进为：

- `POST /api/ai/interpret`
- `GET /api/me`
- `GET /api/records`
- `POST /api/records`
- `PATCH /api/records/:id`
- `GET /api/content/daily`
- `POST /api/billing/checkout`
- `POST /api/webhooks/payment`

---

### 8. 迁移原则

1. 不一次性重写 `index.html`
2. 不在同一轮同时改架构和业务行为
3. 每次迁移后当前入口必须仍可运行
4. 先迁移设计 token，再迁移纯逻辑，再迁移页面结构
5. 涉及商业化能力前，先完成 API、数据、权限和隐私边界设计

推荐迁移顺序：

1. `PRODUCT.md` / `DESIGN.md`
2. `packages/design-system/tokens.css`
3. `packages/domain`
4. `packages/content`
5. `apps/api`
6. `apps/web`

---

### 9. 相关文档

- `PRODUCT.md`
- `DESIGN.md`
- `docs/COMMERCIAL_ARCHITECTURE.md`
- `docs/UI_UX_UPGRADE_PLAN.md`
- `docs/DEVELOPMENT_PLAN.md`
- `docs/PROJECT_STATE.md`
