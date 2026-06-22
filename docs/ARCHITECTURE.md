## 观心（Guān Xīn）项目架构文档

> 最后更新：2026-06-22

---

### 技术栈

前端采用纯原生技术栈，零框架、零构建工具、零包管理器。HTML5 + CSS3（自定义属性 + 关键帧动画）+ Vanilla JavaScript（ES6+），外部依赖仅 Google Fonts CDN（Noto Serif SC + Ma Shan Zheng）和 DashScope API（通义千问 qwen-plus）。

部署平台为 Cloudflare Pages（主）和 GitHub Pages（备），均为纯静态托管。本地开发使用 Python `http.server` 启动的轻量 HTTP 服务器，同时承担 AI API 代理职责。

选型原则遵循 Vibe Coding 方法论："越可验证越好"——选用社区资料丰富、AI 训练数据覆盖充分的成熟技术，不追求前沿。

---

### 目录结构

```
Cculture/
├── index.html          # 主应用文件（SPA 全部代码：HTML + CSS + JS）
├── prototype.html      # 源文件（与 index.html 内容一致，开发用）
├── server.py           # 本地开发服务器 + AI API 代理
├── README.md           # 项目说明
├── .gitignore          # Git 忽略规则
├── AGENTS.md           # AI 编程助手指令（Cursor/Claude Code 等）
│
├── docs/               # 项目文档
│   ├── PRD.md          # 产品需求文档
│   ├── ARCHITECTURE.md # 架构文档（本文件）
│   ├── DEVELOPMENT.md  # 开发规范
│   └── PROJECT_STATE.md # 项目状态（当前进度与待办）
│
├── alm3.py             # [开发补丁] 黄历增强（节气/宜忌/时辰/养生）
├── almanac2.py         # [开发补丁] 黄历季节内容
├── checkin.py          # [开发补丁] 签到徽章
├── friend.py           # [开发补丁] 好友分享
├── h1.py               # [开发补丁] 历史导航按钮
├── history.py          # [开发补丁] 历史屏幕
└── shake.py            # [开发补丁] 竹签摇卦动画
```

说明：`alm3.py` 到 `shake.py` 共 7 个文件为迭代开发过程中产生的补丁脚本（通过字符串替换方式向 prototype.html 注入功能），功能已全部集成到 index.html 中，不再需要运行。保留仅作为开发历史参考。

---

### 代码分层（index.html 内部结构）

index.html 是一个 5364 行的单文件 SPA，内部按以下顺序组织：

**HTML 头部（1-9行）**：DOCTYPE、meta 标签、Google Fonts CDN 引入。

**CSS 样式块（10-1789行，约1780行）**：设计令牌（CSS 自定义属性定义颜色、间距、字体等）、基础重置与排版、各屏幕容器样式、动画关键帧（水墨晕染、竹签摇晃、翻牌3D翻转、加载旋转）、响应式断点（768px / 480px）。

**HTML 主体（1791-2289行，约500行）**：11 个 screen div 容器（splash、birthday、loading、home、daily、shake、result、history、encyclopedia、bazhai、friend），构成应用的页面骨架。

**JavaScript 逻辑（2290-5233行，约2944行）**：数据表（约900行，包含64卦全部数据、天干地支、纳甲、洛书等）、核心算法（八字计算、梅花易数、八宅风水）、数据层（IndexedDB 操作）、业务逻辑（占卦流程、主题分类、七日回顾）、UI 交互（导航、动画、分享）、AI 解读（双路径调用）。

**模态弹窗 HTML（5236-5361行，约126行）**：问题输入模态框、确认对话框、分享面板、数字起卦表单、设置面板、新手引导覆盖层。

---

### 数据模型

#### IndexedDB：占卦记录

数据库 `GuanXinDivination`（v1），对象存储 `records`，主键 `date`（ISO 时间戳字符串）。

记录字段包括：`date`（主键）、`question`（用户问题）、`hexName`（卦名）、`hexIndex`（卦序 0-63）、`upperTri`（上卦 0-7）、`lowerTri`（下卦 0-7）、`changingYao`（变爻 1-6）、`theme`（主题分类：work/relationship/growth/emotion/other）、`favorite`（收藏标记）、`reviewedAt`（七日回顾时间戳）、`summary`（AI 摘要）、`method`（起卦方式：meihua/bamboo/number）。

#### localStorage：轻量设置

共 5 个键：`guanxin_birth`（出生信息 JSON）、`guanxin_onboarded`（引导完成标记）、`guanxin_checkins`（签到日期数组）、`guanxin_apikey`（用户 API Key）、`guanxin_pending_nav`（分享链接延迟导航）。

#### 内存常量：易学数据

全部硬编码在 JS 中（约900行），包括：天干地支及五行映射、纳甲配置、洛书九宫、八卦属性、64卦名及索引映射、象辞（64条）、爻辞（384条）、卦辞+启示（64条）、图鉴标签、主题关键词、命宫描述、流年描述、八宅游星及五行关系。

---

### 外部 API

**DashScope / 通义千问**：使用 `qwen-plus` 模型，通过 OpenAI 兼容的 Chat Completions 接口（`https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions`）进行卦象解读。两条调用路径——服务端代理（server.py 转发，API Key 放 header）和浏览器直连（用户自填 Key，直接 fetch）。

**Google Fonts CDN**：加载 Noto Serif SC（正文）和 Ma Shan Zheng（书法标题）字体。

---

### 屏幕导航

采用自定义 `goTo(screenId)` 函数控制页面切换，通过 CSS class `active` 切换屏幕可见性。无 URL 路由（好友分享除外，通过 URL query params 传递卦象数据）。11 个屏幕按使用频率排列：splash → birthday → loading → home → daily / shake / result / history / encyclopedia / bazhai / friend。

---

### 部署配置

Cloudflare Pages 为主要部署平台（`guanxin-1uu.pages.dev`），GitHub Pages 为备用（`sskks.github.io/guanxin`）。均为纯静态部署，入口文件 `index.html`。本地开发通过 `python server.py` 启动 8080 端口服务器。
