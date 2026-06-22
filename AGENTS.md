# 观心（Guān Xīn）AI 编程助手指令

> 本文件供 Cursor / Claude Code / Windsurf 等 AI 编程工具读取，定义项目上下文和开发规则。

---

## 项目概述

观心是一款基于周易文化的单页 Web 应用（SPA），以古朴水墨风格呈现，融合梅花易数占卦、命宫解读、六十四卦图鉴等功能。纯前端实现，零框架、零构建工具。

## 技术栈

- HTML5 + CSS3 + Vanilla JavaScript (ES6+)
- 无框架、无构建工具、无包管理器
- IndexedDB（占卦记录持久化）+ localStorage（用户设置）
- DashScope API / 通义千问 qwen-plus（AI 解读）
- Google Fonts CDN（Noto Serif SC + Ma Shan Zheng）
- Python http.server（本地开发服务器 + API 代理）
- 部署：Cloudflare Pages + GitHub Pages（纯静态）

## 文件结构

```
index.html      → 主应用（SPA 全部代码，5364行）
prototype.html  → 源文件（与 index.html 一致）
server.py       → 本地服务器 + AI API 代理
docs/           → 项目文档（PRD、架构、规范、状态）
*.py            → 开发补丁脚本（已无运行时用途）
```

## 关键约束

1. **单文件架构**：所有代码在 index.html 中，修改时注意行号区域划分：
   - CSS: 10-1789行
   - HTML 结构: 1791-2289行
   - JS 数据表: 2290-3190行（约）
   - JS 逻辑: 3190-5233行
   - 模态弹窗 HTML: 5236-5361行

2. **不引入新依赖**：不要添加 npm 包、CDN 库、构建工具，除非明确讨论确认

3. **设计风格**：中国水墨风，使用 `:root` 中的 CSS 自定义属性（--ink, --paper, --accent, --gold 等），不要硬编码颜色值

4. **命名规范**：JS 驼峰命名、CSS 类名 kebab-case、常量 UPPER_SNAKE

5. **语言**：注释用中文，提交消息用中文

## 开发规则

- 只修改明确指定的文件和代码区域
- 不要擅自重构或重新组织已有代码
- 不要将单文件拆分为多文件，除非明确讨论确认
- 新增易学数据必须验证准确性
- 不提交 API Key 或敏感信息
- 每次提交是一个"可验证的小切片"
- 提交前在浏览器中验证：控制台无报错、功能正常、移动端适配正常

## 提交消息格式

```
<type>: <简短描述>

[可选详细说明]
```

type: feat / fix / style / docs / refactor / perf / chore

## 项目文档

详细文档在 `docs/` 目录：
- `docs/PRD.md` — 产品需求文档（功能清单、用户流程、验收标准）
- `docs/ARCHITECTURE.md` — 架构文档（技术栈、目录结构、数据模型）
- `docs/DEVELOPMENT.md` — 开发规范（命名、代码风格、验证清单）
- `docs/PROJECT_STATE.md` — 项目状态（当前进度、技术债、待办）
