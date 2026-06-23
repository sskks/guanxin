# Design

## Identity

观心当前视觉系统是水墨纸感、朱砂强调、青玉辅助、低饱和墨色文字的东方产品界面。后续升级要保留文化气质，但从“古风展示”转向“情绪产品 UI”：更清晰、更可读、更有行动引导。

## Color Tokens

当前运行入口 `index.html` 已定义基础色彩令牌，后续拆分时必须先迁移这些 token，而不是在组件中硬编码颜色。

| Role | Current token | Current value | Usage |
| --- | --- | --- | --- |
| Background | `--paper` | `#F2EBD9` | 页面背景 |
| Surface | `--paper-light` | `#F8F3E6` | 表单、卡片、浮层 |
| Surface Alt | `--paper-dark` | `#E5DCC8` | 次级底色、步骤条 |
| Primary Text | `--ink-deep` | `#2C2418` | 标题、重要内容 |
| Body Text | `--ink` | `#4A3F30` | 正文 |
| Muted Text | `--ink-light` | `#7A6E5C` | 辅助说明 |
| Border | `--ink-ghost` | `#D8CEBC` | 边框、分隔线 |
| Primary Accent | `--cinnabar` | `#A83C32` | 主按钮、重点状态 |
| Support Accent | `--jade` | `#6A8E6E` | AI、成长、完成状态 |
| Warm Accent | `--gold` | `#8B7355` | 标签、提示、次级强调 |

## Color Direction

现有色彩偏暖纸色。继续使用时要避免整页变成低对比“泛黄纸面”。升级方向：

- 主体内容区保持纸感，但重要操作区提高对比度
- 朱砂只用于主行动、当前状态和关键提醒
- 青玉用于“安顿、完成、回看、AI 解读”等舒缓状态
- 金色只用于辅助标签，不承担主要可点击状态
- 弱文本不得低于可读对比度

## Typography

现有字体：

- 标题/书法感：`Ma Shan Zheng`
- 中文正文：`Noto Serif SC`
- UI 基础：已有 `--font-sans` / `--font-serif` / `--font-display`

后续规则：

- 页面标题可保留书法字体，但按钮、表单、标签、导航不要使用过强书法感
- 正文字号移动端不低于 16px
- 长段解释行高保持 1.65-1.9
- 功能页面内部标题不要使用过大的 display 字号
- 不使用负 letter-spacing

## Layout

产品是移动优先的 SPA，核心布局约束：

- 375px 宽度为主要验收视口
- 内容最大宽度建议 560px
- 功能页顶部保留明确导航区
- 结果页先展示结论和下一步，再展示传统文本
- 页面段落采用清晰分区，不使用卡片套卡片
- 底部分享、收藏、回看等行动保持同一组件语言

## Components

必须优先统一以下组件：

- `TopBar`：左上返回、页面标题、右侧设置或帮助入口
- `ActionCard`：AI 结论、建议行动、今日避免、一句话提醒
- `NextStepPanel`：收藏、回看、继续学习、分享
- `TermExplain`：术语白话说明，例如命宫、卦、爻、变卦
- `Toast`：成功、失败、恢复路径提示
- `ModalSheet`：移动端优先的表单和确认面板

组件状态必须包含：

- default
- hover / pressed
- focus
- disabled
- loading
- error
- selected

## Motion

动效服务于“状态变化”和“空间方向”：

- 页面前进可轻微向左或向上进入
- 返回可向右或向下退出
- AI 加载使用低干扰进度反馈
- 收藏、完成、回看标记使用 150-250ms 微反馈
- 支持 `prefers-reduced-motion: reduce`
- 不使用纯装饰型大面积动画

## Navigation

导航是第一阶段最高优先级体验之一：

- 关键页面返回按钮统一在左上角
- 返回逻辑优先上一页，不默认回首页
- 移动端关键页面支持右滑返回，但必须保留可见按钮
- 模态与浮层必须支持关闭和 Esc
- 所有返回行为要与浏览器历史或内部导航栈保持一致

## UX Copy

默认文案顺序：

1. 白话结论
2. 和当前处境的关系
3. 今天能做什么
4. 今天先不要做什么
5. 传统术语和出处

禁止把术语作为第一层解释。AI 输出必须避免大段铺陈，优先短句和行动。

## Responsive Requirements

- 375px、768px、1440px 三个宽度必须验收
- 不出现水平滚动
- 弹窗宽度不超过视口减 32px
- 固定顶部/底部区域不得遮挡内容
- 触控目标不小于 44px

## Implementation Notes

当前 `index.html` 是唯一真实运行入口。设计系统落地顺序：

1. 将 `:root` token 抽到 `packages/design-system/tokens.css`
2. 将通用组件样式抽到 `packages/design-system/components.css`
3. 将页面样式拆到 `apps/web/styles/`
4. 保持 `index.html` 可运行，逐步迁移，不一次性重写
