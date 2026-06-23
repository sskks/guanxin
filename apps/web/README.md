# apps/web

未来前端应用目录。

当前状态：

- 线上真实入口仍是项目根目录的 `index.html`
- 本目录先作为前端拆分目标，不参与运行
- 后续按页面、组件、样式、状态管理逐步迁移

推荐迁移顺序：

1. `packages/design-system/tokens.css`
2. `packages/design-system/components.css`
3. `apps/web/styles/`
4. `apps/web/pages/`
5. `apps/web/features/`

迁移原则：

- 每次迁移后根目录 `index.html` 仍必须可运行
- 不在同一轮同时改架构和业务逻辑
- 不引入构建工具，除非完成技术方案评审
