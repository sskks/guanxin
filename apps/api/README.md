# apps/api

未来后端服务目录。

当前状态：

- 根目录 `server.py` 仍是当前本地开发服务器和 AI 代理
- 本目录用于承接商业化阶段需要的后端能力
- 暂不引入数据库和账号依赖，避免破坏现有 MVP

后端能力演进顺序：

1. AI 代理标准化：模型、限流、错误码、日志
2. 用户系统：匿名用户、登录用户、第三方登录
3. 数据同步：占卦记录、收藏、回看、设置
4. 支付与权益：订阅、额度、会员权益
5. 内容管理：图鉴、节气、今日一问、运营内容
6. 风控与合规：隐私、审计、敏感内容边界

建议 API 边界：

- `POST /api/ai/interpret`
- `GET /api/me`
- `GET /api/records`
- `POST /api/records`
- `PATCH /api/records/:id`
- `GET /api/content/daily`
- `POST /api/billing/checkout`
- `POST /api/webhooks/payment`
