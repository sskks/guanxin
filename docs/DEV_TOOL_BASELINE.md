# 开发工具基线

更新日期：2026-06-30

## 当前可用工具

- `python`：可用，已验证 `python -m py_compile .\server.py`
- `node`：可用
- `npm`：可用
- `npx`：可用
- `git`：可用
- `gh`：已安装，但当前未登录
- `rg`：可用

## 当前依赖形态

- 当前工作区没有根级 `package.json`
- 现阶段主运行入口仍是根目录 `index.html` + `server.py`
- `apps/` 与 `packages/` 目前是演进骨架，不是当前运行时依赖来源

结论：

- 今天不需要执行 `npm install`
- 当前工具准备重点是命令可用、仓库可控、文档可追踪

## GitHub 协作方式

当前项目采用双通道：

- 本地版本控制与代码提交：`git`
- 仓库、PR、Issue 查询与后续协作：GitHub 插件能力优先

说明：

- GitHub 插件适合做仓库查看、PR/Issue 处理、后续发布协作
- 本地开发、差异核对、提交与回滚仍以本地 `git` 为基础

## 本地仓库状态

当前工作目录：

- `D:\vscode\Microsoft VS Code\project\Cculture`

已完成：

- 当前目录已重新接回远端仓库 `https://github.com/sskks/guanxin.git`
- 当前分支：`main`
- 当前远端跟踪：`origin/main`
- 已验证 `git fetch origin --prune` 可执行
- 已验证 `git push --dry-run origin main` 可执行

接回方式说明：

- 先从远端仓库拉取只读快照
- 再将快照中的 `.git` 目录复制回当前工作目录
- 该操作只恢复版本历史与远端配置，不覆盖业务文件

## 当前已知状态

- 当前工作区不是干净状态，存在一批历史改动
- `git diff --name-only` 目前显示的明确内容差异主要在 `index.html`
- 同时存在 3 个未跟踪文档：
  - `docs/PAGE_SPEC_V1.md`
  - `docs/SKILL_ORCHESTRATION_AND_GITHUB_ADOPTION.md`
  - `docs/STAGE_PROGRESS_2026-06-30.md`
- 多个文件存在 `LF -> CRLF` 提示，提交前需要再次确认实际差异范围，避免把行尾变更误带入提交

## 当前阻塞项

- `gh auth status` 显示当前未登录

影响：

- 不影响本地开发与 `git fetch`
- 不影响通过本地 `git` 进行常规推送
- 可能影响后续通过 `gh` 直接创建 PR、查看 Actions、执行 GitHub CLI 写操作

建议：

- 后续如果要走 `gh` 命令流，再单独补一次登录
- 如果只做仓库查看、PR/Issue 查询，可优先使用 GitHub 插件能力

## 今日工具准备结论

当前已经具备继续开发所需的最小工具闭环：

- 可本地运行：`python`
- 可继续前端/脚本开发：`node` / `npm`
- 可恢复版本管理：`git`
- 可接入仓库协作：GitHub 插件

因此下一阶段可以直接进入功能开发与 UI 重构，不需要继续停留在环境安装阶段。
