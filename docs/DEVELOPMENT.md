## 观心（Guān Xīn）开发规范

> 供所有开发者（包括 AI 编程助手）遵循

---

### 编程语言与版本

HTML5、CSS3、Vanilla JavaScript（ES6+）。不使用 TypeScript，不使用任何框架（React/Vue/Angular 等），不使用构建工具（Webpack/Vite 等）。Python 3.x 仅用于本地开发服务器。

---

### 命名约定

JavaScript 变量和函数使用驼峰命名（camelCase），如 `calcBaZhai`、`showDivResult`。CSS 类名使用中划线连接（kebab-case），如 `shake-screen`、`flip-card`。HTML id 使用中划线连接，如 `home-screen`、`enc-grid`。常量使用全大写下划线（UPPER_SNAKE），如 `TRIGRAM_ATTR`、`THEME_KEYWORDS`。文件名全部小写。

---

### 代码风格

缩进使用 2 个空格（与现有代码保持一致）。JavaScript 使用 `let` / `const`，不使用 `var`。字符串使用单引号。模板字符串（反引号）用于多行 HTML 拼接。CSS 自定义属性统一在 `:root` 中定义设计令牌，禁止在组件样式中硬编码颜色值。

注释使用中文，格式为 `// 功能说明` 或 `/* 多行说明 */`。每个函数前应有简要说明其用途的单行注释。

---

### 文件与模块规则

当前真实运行入口仍为单文件 SPA（`index.html`）。同时，项目已经建立 `apps/` 与 `packages/` 架构骨架，用于后续商业化演进。

开发时遵循两条规则：

- 当前功能修复和体验优化优先改 `index.html`
- 架构迁移和新模块沉淀优先放入 `apps/` / `packages/`

修改 `index.html` 时遵循以下约束：

CSS 区域修改范围在第 10-1789 行。HTML 结构区域在第 1791-2289 行。JavaScript 数据表区域在第 2290-3190 行（约），修改前务必核对卦序和索引。JavaScript 逻辑区域在第 3190-5233 行。模态弹窗 HTML 在第 5236-5361 行。

新增功能时，CSS 样式追加到对应屏幕样式块末尾，JS 函数追加到相关功能函数组末尾。不要重新排列已有代码的顺序。

架构迁移时遵循以下约束：

- `packages/design-system` 只放设计 token、组件样式和设计规则
- `packages/domain` 只放纯数据和纯函数，不访问 DOM
- `packages/content` 只放内容、术语、prompt 和运营文本
- `apps/api` 只放后端服务相关内容
- `apps/web` 只放未来前端应用结构
- 迁移后必须保证 `index.html` 仍可运行

---

### 提交规范

提交消息格式：

```
<type>: <简短描述>

[可选的详细说明]
```

type 取值：`feat`（新功能）、`fix`（修复）、`style`（纯样式调整）、`docs`（文档）、`refactor`（重构）、`perf`（性能优化）、`chore`（杂项）。

示例：
```
feat: 添加月相显示到每日一卦

在每日一卦页面增加当前月相图标和农历日期显示，
使用天文算法库计算朔望月周期。
```

每次提交应为一个"可验证的小切片"——不要一次提交多个不相关改动。

---

### Git 分支策略

`main` 为稳定分支，始终保持可部署状态。新功能在独立分支开发：`feat/<功能名>`（如 `feat/moon-phase`）。修复在 `fix/<问题描述>` 分支。完成后合并到 main 并推送。

---

### 验证清单

每次提交前，逐项确认：

- [ ] 在浏览器中打开 index.html，控制台无红色报错
- [ ] 新增功能手动测试通过（按 PRD 验收标准）
- [ ] 已有功能未被破坏（回归测试核心流程：每日一卦、问易、摇卦、数字起卦、历史、图鉴）
- [ ] 移动端（375px 宽）和桌面端（1440px 宽）均正常显示
- [ ] 无硬编码的 API Key 或敏感信息提交
- [ ] 若修改 UI，符合 `DESIGN.md` 和 `docs/UI_UX_UPGRADE_PLAN.md`
- [ ] 若修改架构，更新 `docs/ARCHITECTURE.md` 或 `docs/COMMERCIAL_ARCHITECTURE.md`

---

### AI 编程助手特别规则

1. 只修改明确指定的文件和代码区域，不要擅自重构或重新组织已有代码
2. 不要引入新的外部依赖（npm 包、CDN 库等），除非明确讨论并确认
3. 不要一次性将单文件 SPA 拆分为多文件；允许按文档规划建立迁移骨架和逐步抽离
4. 新增的易学数据（卦辞、爻辞等）必须经过交叉验证准确性
5. 涉及 API Key 的代码不要包含实际密钥，使用占位符
6. 生成的 CSS 必须使用 `:root` 中已定义的设计令牌，不要硬编码颜色
7. 所有新功能必须有对应的中文注释说明
8. UI 迭代优先解决可返回、可理解、可行动三个问题
