# Skills 分类索引

按用途整理的用户级 AI Agent 技能副本，涵盖产品、工程、测试、内容制作与平台集成。下表可直接跳转到各分类，分类内的技能链接指向对应 `SKILL.md`。

当前包含 **17 个分类、254 个不同目录名、281 个分类副本**。同一技能可出现在多个分类中；`gstack-` 前缀入口单独计数，但通常与无前缀入口对应同一工作流。

## 分类总览

| 分类 | 技能入口数 | 主要内容 |
| --- | ---: | --- |
| [产品设计与需求 · `product`](#product) | 30 | 产品构思、需求访谈、规格编写、原型探索和体验评审。 |
| [项目管理 · `project`](#project) | 30 | 项目规划、任务拆分、协作交接、进度恢复、复盘和发布管理。 |
| [架构设计 · `architecture`](#architecture) | 26 | 系统架构、领域建模、模块边界、依赖分析和技术架构图。 |
| [前端设计 · `frontend`](#frontend) | 20 | 网页视觉、UI/UX、设计系统、交互原型和网页动画。 |
| [后端开发 · `backend`](#backend) | 35 | 适用于后端的通用实现、服务集成、调试、安全、代码审查和重构技能。 |
| [功能测试与验证 · `test`](#test) | 33 | Web/iOS 功能验证、浏览器测试、性能回归、视觉检查和测试质量。 |
| [视频制作 · `video`](#video) | 13 | HTML 视频、程序化动画、AI 视频生成、宣传片复刻与剪辑。 |
| [文章与文档 · `article`](#article) | 10 | 文章构思、技术博客、项目文档维护和 PDF 导出。 |
| [浏览器与采集 · `browser`](#browser) | 11 | 平台内容读取、浏览器连接、网页采集和桌面应用操作。 |
| [搜索与研究 · `research`](#research) | 3 | 实时检索、系统研究和多 AI 平台结果比较。 |
| [股票与金融 · `finance`](#finance) | 4 | A 股分析、金融数据查询、概念事件归档和雪球访问配置。 |
| [智能体与协作 · `agent`](#agent) | 14 | Agent 管理、模型第二意见、模型比较、团队知识与上下文管理。 |
| [移动端工具 · `mobile`](#mobile) | 4 | iOS 调试桥清理与同步；iOS 测试和视觉审查技能另见 test 分类。 |
| [知识与教学 · `knowledge`](#knowledge) | 3 | 网页笔记归档、学习引导和课程练习目录生成。 |
| [逆向工程 · `reverse`](#reverse) | 2 | 基于发布产物和运行证据的逆向分析，以及专项技能路由。 |
| [工具与配置 · `tooling`](#tooling) | 16 | 技能路由、方案质询、操作保护、编辑范围和工具升级。 |
| [飞书集成 · `lark`](#lark) | 27 | 飞书消息、文档、表格、日程、会议、审批、任务和应用开发。 |

## 阅读与使用说明

- 每个分类的技能位于 `<分类>/.agents/skills/<技能目录>/`，点击技能名可查看具体触发条件、操作步骤和依赖。
- 表格按目录名标识技能。部分目录名与技能声明的名称不同，例如 `taste-skill` 声明为 `design-taste-frontend`、`visual-cards` 声明为 `create-visual-card`。
- 同分类中通常将无前缀与 `gstack-` 前缀入口合并展示，并保留两个链接；内容或用途不同的入口分别说明。
- 这些目录保存的是技能说明及配套文件。部分技能仍依赖本机 CLI、浏览器、MCP、API 授权或用户级工具；复制文件不等于已安装全部运行依赖。
- 软链接已复制为实际文件，Git 历史、虚拟环境和依赖缓存未收录；两个 gstack 历史备份目录未收录。

<a id="product"></a>

## 产品设计与需求（product）

产品构思、需求访谈、规格编写、原型探索和体验评审。

目录：[`product/.agents/skills/`](product/.agents/skills/) · 30 个技能入口。

| 技能 | 概要简介 |
| --- | --- |
| [`brainstorm`](product/.agents/skills/brainstorm/SKILL.md) | 通过协作讨论探索模糊想法，发现需求和候选方案。 |
| [`design-consultation`](product/.agents/skills/design-consultation/SKILL.md) / [`gstack-design-consultation`](product/.agents/skills/gstack-design-consultation/SKILL.md) | 结合产品与竞品研究，制定字体、颜色、布局和动效等设计系统。 |
| [`design-shotgun`](product/.agents/skills/design-shotgun/SKILL.md) / [`gstack-design-shotgun`](product/.agents/skills/gstack-design-shotgun/SKILL.md) | 生成多个设计方案，通过对比和反馈迭代选定方向。 |
| [`domain-modeling`](product/.agents/skills/domain-modeling/SKILL.md) | 梳理领域术语、领域模型、CONTEXT.md 和架构决策记录。 |
| [`grill-me`](product/.agents/skills/grill-me/SKILL.md) | 通过持续追问澄清并打磨计划或设计。 |
| [`grill-with-docs`](product/.agents/skills/grill-with-docs/SKILL.md) | 在质询方案的同时记录术语表与架构决策等文档。 |
| [`grilling`](product/.agents/skills/grilling/SKILL.md) | 通过深入访谈检验计划、决策和想法中的假设。 |
| [`gstack-office-hours`](product/.agents/skills/gstack-office-hours/SKILL.md) | 通过创业或个人项目模式澄清需求、判断构建价值并形成设计文档。 |
| [`gstack-plan-ceo-review`](product/.agents/skills/gstack-plan-ceo-review/SKILL.md) | 从产品和战略角度质询方案，评估范围、目标和产品潜力。 |
| [`gstack-plan-design-review`](product/.agents/skills/gstack-plan-design-review/SKILL.md) | 在实现前评审 UI/UX 方案，评分并完善设计细节。 |
| [`gstack-plan-devex-review`](product/.agents/skills/gstack-plan-devex-review/SKILL.md) | 评审 API、CLI、SDK、文档和平台的开发者体验与接入流程。 |
| [`gstack-spec`](product/.agents/skills/gstack-spec/SKILL.md) | 将模糊意图逐步转化为明确、可执行的规格与 Issue。 |
| [`html-plan`](product/.agents/skills/html-plan/SKILL.md) | 将计划整理成结构清晰、便于阅读的自包含 HTML 页面。 |
| [`huashu-design`](product/.agents/skills/huashu-design/SKILL.md) | 以多方向方案探索制作高保真 HTML 原型、演示、动画和可视化。 |
| [`loop-me`](product/.agents/skills/loop-me/SKILL.md) | 通过访谈梳理待构建工作流的规格。 |
| [`office-hours`](product/.agents/skills/office-hours/SKILL.md) / [`gstack-office-hours`](product/.agents/skills/gstack-office-hours/SKILL.md) | 通过创业或个人项目模式澄清需求、判断构建价值并形成设计文档。 |
| [`plan-ceo-review`](product/.agents/skills/plan-ceo-review/SKILL.md) / [`gstack-plan-ceo-review`](product/.agents/skills/gstack-plan-ceo-review/SKILL.md) | 从产品和战略角度质询方案，评估范围、目标和产品潜力。 |
| [`plan-design-review`](product/.agents/skills/plan-design-review/SKILL.md) / [`gstack-plan-design-review`](product/.agents/skills/gstack-plan-design-review/SKILL.md) | 在实现前评审 UI/UX 方案，评分并完善设计细节。 |
| [`plan-devex-review`](product/.agents/skills/plan-devex-review/SKILL.md) / [`gstack-plan-devex-review`](product/.agents/skills/gstack-plan-devex-review/SKILL.md) | 评审 API、CLI、SDK、文档和平台的开发者体验与接入流程。 |
| [`prototype`](product/.agents/skills/prototype/SKILL.md) | 构建临时原型，验证界面、状态模型或业务逻辑的设计假设。 |
| [`research`](product/.agents/skills/research/SKILL.md) | 依据可信的一手来源研究问题，并将结果保存为 Markdown。 |
| [`spec`](product/.agents/skills/spec/SKILL.md) / [`gstack-spec`](product/.agents/skills/gstack-spec/SKILL.md) | 将模糊意图逐步转化为明确、可执行的规格与 Issue。 |
| [`to-questionnaire`](product/.agents/skills/to-questionnaire/SKILL.md) | 将尚未解决的决策整理成供他人填写的问卷。 |
| [`to-spec`](product/.agents/skills/to-spec/SKILL.md) | 将已有讨论综合为规格，并发布到项目 Issue 跟踪系统。 |
| [`to-tickets`](product/.agents/skills/to-tickets/SKILL.md) | 把计划或规格拆成可渐进交付的任务单，并标注阻塞依赖。 |
| [`triage`](product/.agents/skills/triage/SKILL.md) | 对 Issue 和外部 PR 进行分类、核实、澄清并形成可执行任务说明。 |
| [`ui-ux-pro-max`](product/.agents/skills/ui-ux-pro-max/SKILL.md) | 提供跨技术栈的 UI/UX 风格、配色、字体、组件、可访问性与布局参考。 |
| [`wayfinder`](product/.agents/skills/wayfinder/SKILL.md) | 将大型工作拆为关联的决策任务图，逐项解决关键决策。 |

<a id="project"></a>

## 项目管理（project）

项目规划、任务拆分、协作交接、进度恢复、复盘和发布管理。

目录：[`project/.agents/skills/`](project/.agents/skills/) · 30 个技能入口。

| 技能 | 概要简介 |
| --- | --- |
| [`autoplan`](project/.agents/skills/autoplan/SKILL.md) / [`gstack-autoplan`](project/.agents/skills/gstack-autoplan/SKILL.md) | 串联产品、设计、工程和开发者体验评审，自动处理常规决策。 |
| [`claude-handoff`](project/.agents/skills/claude-handoff/SKILL.md) | 把当前会话工作移交给新的后台 Agent 继续执行。 |
| [`codeup-merge-request`](project/.agents/skills/codeup-merge-request/SKILL.md) | 推送分支并创建或复用阿里云 Codeup 合并请求。 |
| [`context-restore`](project/.agents/skills/context-restore/SKILL.md) / [`gstack-context-restore`](project/.agents/skills/gstack-context-restore/SKILL.md) | 恢复之前保存的上下文、进度和下一步工作。 |
| [`context-save`](project/.agents/skills/context-save/SKILL.md) / [`gstack-context-save`](project/.agents/skills/gstack-context-save/SKILL.md) | 保存当前 Git 状态、工作进展、决策和未完成任务。 |
| [`git-guardrails-claude-code`](project/.agents/skills/git-guardrails-claude-code/SKILL.md) | 为 Claude Code 配置钩子，拦截危险 Git 命令。 |
| [`gstack-land-and-deploy`](project/.agents/skills/gstack-land-and-deploy/SKILL.md) | 合并 PR、等待 CI 与部署，并验证生产环境状态。 |
| [`gstack-landing-report`](project/.agents/skills/gstack-landing-report/SKILL.md) | 只读查看版本槽位、待发布 PR 和相关工作区的发布队列。 |
| [`gstack-retro`](project/.agents/skills/gstack-retro/SKILL.md) | 分析提交历史、团队贡献和工作模式，生成周度工程复盘与趋势记录。 |
| [`gstack-setup-deploy`](project/.agents/skills/gstack-setup-deploy/SKILL.md) | 识别部署平台并记录部署命令、线上地址和健康检查配置。 |
| [`gstack-ship`](project/.agents/skills/gstack-ship/SKILL.md) | 执行测试、审查、版本与变更日志更新、提交、推送及 PR 创建流程。 |
| [`handoff`](project/.agents/skills/handoff/SKILL.md) | 把当前讨论压缩为供其他 Agent 继续工作的交接文档。 |
| [`land-and-deploy`](project/.agents/skills/land-and-deploy/SKILL.md) / [`gstack-land-and-deploy`](project/.agents/skills/gstack-land-and-deploy/SKILL.md) | 合并 PR、等待 CI 与部署，并验证生产环境状态。 |
| [`landing-report`](project/.agents/skills/landing-report/SKILL.md) / [`gstack-landing-report`](project/.agents/skills/gstack-landing-report/SKILL.md) | 只读查看版本槽位、待发布 PR 和相关工作区的发布队列。 |
| [`orchestration`](project/.agents/skills/orchestration/SKILL.md) | 协调 Orca 多 Agent 任务、依赖、消息、决策与执行状态。 |
| [`pm`](project/.agents/skills/pm/SKILL.md) | 按 PDCA 循环进行任务规划、进度跟踪和上下文管理。 |
| [`pr`](project/.agents/skills/pr/SKILL.md) | 编写便于审查者理解问题、变更和验证结果的 PR 描述。 |
| [`project-handoff`](project/.agents/skills/project-handoff/SKILL.md) | 生成跨项目交接文档，保留目标、用户要求、进度、证据和下一步。 |
| [`resolving-merge-conflicts`](project/.agents/skills/resolving-merge-conflicts/SKILL.md) | 分析并解决正在进行的 Git 合并或变基冲突。 |
| [`retro`](project/.agents/skills/retro/SKILL.md) | 复盘当前编码会话，总结执行过程与改进点。 |
| [`setup-deploy`](project/.agents/skills/setup-deploy/SKILL.md) / [`gstack-setup-deploy`](project/.agents/skills/gstack-setup-deploy/SKILL.md) | 识别部署平台并记录部署命令、线上地址和健康检查配置。 |
| [`setup-matt-pocock-skills`](project/.agents/skills/setup-matt-pocock-skills/SKILL.md) | 配置工程技能所需的 Issue 跟踪器、分诊标签和领域文档布局。 |
| [`ship`](project/.agents/skills/ship/SKILL.md) / [`gstack-ship`](project/.agents/skills/gstack-ship/SKILL.md) | 执行测试、审查、版本与变更日志更新、提交、推送及 PR 创建流程。 |
| [`to-tickets`](project/.agents/skills/to-tickets/SKILL.md) | 把计划或规格拆成可渐进交付的任务单，并标注阻塞依赖。 |
| [`triage`](project/.agents/skills/triage/SKILL.md) | 对 Issue 和外部 PR 进行分类、核实、澄清并形成可执行任务说明。 |
| [`wayfinder`](project/.agents/skills/wayfinder/SKILL.md) | 将大型工作拆为关联的决策任务图，逐项解决关键决策。 |
| [`wizard`](project/.agents/skills/wizard/SKILL.md) | 为需要人工完成的配置、凭据或迁移步骤生成交互式 Bash 向导。 |

<a id="architecture"></a>

## 架构设计（architecture）

系统架构、领域建模、模块边界、依赖分析和技术架构图。

目录：[`architecture/.agents/skills/`](architecture/.agents/skills/) · 26 个技能入口。

| 技能 | 概要简介 |
| --- | --- |
| [`archify`](architecture/.agents/skills/archify/SKILL.md) | 生成带主题切换和图片导出的 HTML/SVG 架构图、流程图、时序图与状态图。 |
| [`architecture-review`](architecture/.agents/skills/architecture-review/SKILL.md) | 检查大型模块、静默失败、类型安全和测试缺口等代码结构问题。 |
| [`brooks-audit`](architecture/.agents/skills/brooks-audit/SKILL.md) | 分析模块依赖、分层、循环引用和架构退化，支持代码库导览。 |
| [`brooks-debt`](architecture/.agents/skills/brooks-debt/SKILL.md) | 识别并评估技术债，按影响和维护成本制定重构优先级。 |
| [`bruce-drawio`](architecture/.agents/skills/bruce-drawio/SKILL.md) | 生成可编辑的 draw.io XML，并通过 CLI 导出 PNG、SVG 或 PDF。 |
| [`build-graph`](architecture/.agents/skills/build-graph/SKILL.md) | 建立或更新代码审查知识图谱，为导航和影响分析提供基础。 |
| [`clean-architecture`](architecture/.agents/skills/clean-architecture/SKILL.md) | 按整洁架构检查依赖方向、分层边界和 SOLID 原则。 |
| [`codebase-design`](architecture/.agents/skills/codebase-design/SKILL.md) | 运用深模块理念设计接口、模块边界和可测试的代码结构。 |
| [`deslop-shared-libs`](architecture/.agents/skills/deslop-shared-libs/SKILL.md) / [`gstack-deslop-shared-libs`](architecture/.agents/skills/gstack-deslop-shared-libs/SKILL.md) | 分析近期代码，推荐值得抽取的共享逻辑和公共库。 |
| [`diagram`](architecture/.agents/skills/diagram/SKILL.md) / [`gstack-diagram`](architecture/.agents/skills/gstack-diagram/SKILL.md) | 把自然语言或 Mermaid 转为图源、可编辑 Excalidraw，以及 SVG/PNG。 |
| [`domain-modeling`](architecture/.agents/skills/domain-modeling/SKILL.md) | 梳理领域术语、领域模型、CONTEXT.md 和架构决策记录。 |
| [`drawio`](architecture/.agents/skills/drawio/SKILL.md) | 制作 draw.io 架构图、流程图、UML、ER 图和线框图，并支持导出。 |
| [`explore-codebase`](architecture/.agents/skills/explore-codebase/SKILL.md) | 通过知识图谱理解代码结构、模块关系和关键实现。 |
| [`fireworks-tech-graph`](architecture/.agents/skills/fireworks-tech-graph/SKILL.md) | 生成技术架构图、数据流、时序图和概念图，导出 SVG/PNG。 |
| [`gstack-plan-eng-review`](architecture/.agents/skills/gstack-plan-eng-review/SKILL.md) | 评审技术方案中的架构、数据流、边界条件、测试与性能设计。 |
| [`html-diagram`](architecture/.agents/skills/html-diagram/SKILL.md) | 制作自包含 HTML 架构说明页，以 SVG 展示系统和技术栈关系。 |
| [`improve-codebase-architecture`](architecture/.agents/skills/improve-codebase-architecture/SKILL.md) | 扫描模块改进机会，生成可视化报告并逐项讨论设计方案。 |
| [`omm-push`](architecture/.agents/skills/omm-push/SKILL.md) | 将架构文档推送到 oh-my-mermaid 云端，处理登录和项目关联。 |
| [`omm-scan`](architecture/.agents/skills/omm-scan/SKILL.md) | 扫描代码架构，生成或更新 .omm 架构文档和图表。 |
| [`omm-view`](architecture/.agents/skills/omm-view/SKILL.md) | 启动 oh-my-mermaid 网页查看器，浏览架构图。 |
| [`plan-eng-review`](architecture/.agents/skills/plan-eng-review/SKILL.md) / [`gstack-plan-eng-review`](architecture/.agents/skills/gstack-plan-eng-review/SKILL.md) | 评审技术方案中的架构、数据流、边界条件、测试与性能设计。 |
| [`prompt-harness-architect`](architecture/.agents/skills/prompt-harness-architect/SKILL.md) | 设计 LLM 应用的系统提示词、上下文、历史消息和评估策略。 |
| [`refactor-safely`](architecture/.agents/skills/refactor-safely/SKILL.md) | 结合依赖分析和影响范围，规划并执行安全重构。 |
| [`setup-ts-deep-modules`](architecture/.agents/skills/setup-ts-deep-modules/SKILL.md) | 为 TypeScript 配置 dependency-cruiser，约束模块通过入口文件暴露实现。 |

<a id="frontend"></a>

## 前端设计（frontend）

网页视觉、UI/UX、设计系统、交互原型和网页动画。

目录：[`frontend/.agents/skills/`](frontend/.agents/skills/) · 20 个技能入口。

| 技能 | 概要简介 |
| --- | --- |
| [`design-consultation`](frontend/.agents/skills/design-consultation/SKILL.md) / [`gstack-design-consultation`](frontend/.agents/skills/gstack-design-consultation/SKILL.md) | 结合产品与竞品研究，制定字体、颜色、布局和动效等设计系统。 |
| [`design-html`](frontend/.agents/skills/design-html/SKILL.md) / [`gstack-design-html`](frontend/.agents/skills/gstack-design-html/SKILL.md) | 把设计方案实现为基于 Pretext 的 HTML/CSS 页面。 |
| [`design-review`](frontend/.agents/skills/design-review/SKILL.md) / [`gstack-design-review`](frontend/.agents/skills/gstack-design-review/SKILL.md) | 检查并修复视觉层级、间距、一致性、交互和模板化设计问题。 |
| [`design-shotgun`](frontend/.agents/skills/design-shotgun/SKILL.md) / [`gstack-design-shotgun`](frontend/.agents/skills/gstack-design-shotgun/SKILL.md) | 生成多个设计方案，通过对比和反馈迭代选定方向。 |
| [`frontend-design`](frontend/.agents/skills/frontend-design/SKILL.md) | 为新建或改版 UI 提供视觉方向、排版和具有辨识度的设计指导。 |
| [`gsap`](frontend/.agents/skills/gsap/SKILL.md) | 提供 GSAP 动画、缓动、时间线和性能参考，主要服务 HyperFrames 动画。 |
| [`gstack-plan-design-review`](frontend/.agents/skills/gstack-plan-design-review/SKILL.md) | 在实现前评审 UI/UX 方案，评分并完善设计细节。 |
| [`html`](frontend/.agents/skills/html/SKILL.md) | 制作自包含 HTML 报告、解释页、演示文稿或原型。 |
| [`huashu-design`](frontend/.agents/skills/huashu-design/SKILL.md) | 以多方向方案探索制作高保真 HTML 原型、演示、动画和可视化。 |
| [`plan-design-review`](frontend/.agents/skills/plan-design-review/SKILL.md) / [`gstack-plan-design-review`](frontend/.agents/skills/gstack-plan-design-review/SKILL.md) | 在实现前评审 UI/UX 方案，评分并完善设计细节。 |
| [`prototype`](frontend/.agents/skills/prototype/SKILL.md) | 构建临时原型，验证界面、状态模型或业务逻辑的设计假设。 |
| [`super-frontend-design`](frontend/.agents/skills/super-frontend-design/SKILL.md) | 构建注重视觉质量的前端页面，结合 SVG 图标与真实摄影素材。 |
| [`taste-skill`](frontend/.agents/skills/taste-skill/SKILL.md) | 根据需求选择视觉方向，制作减少模板化观感的前端界面和改版设计。 |
| [`ui-ux-pro-max`](frontend/.agents/skills/ui-ux-pro-max/SKILL.md) | 提供跨技术栈的 UI/UX 风格、配色、字体、组件、可访问性与布局参考。 |
| [`visual-cards`](frontend/.agents/skills/visual-cards/SKILL.md) | 把内容制作成自包含 HTML 视觉卡片，并截图导出 PNG。 |
| [`web-design`](frontend/.agents/skills/web-design/SKILL.md) | 根据 PRD、参考网站或截图生成 DESIGN.md，再实现网页视觉、交互与响应式布局。 |

<a id="backend"></a>

## 后端开发（backend）

适用于后端的通用实现、服务集成、调试、安全、代码审查和重构技能。

目录：[`backend/.agents/skills/`](backend/.agents/skills/) · 35 个技能入口。

| 技能 | 概要简介 |
| --- | --- |
| [`brooks-review`](backend/.agents/skills/brooks-review/SKILL.md) | 从可维护性、设计异味和代码退化角度审查代码与 PR，并给出改进建议。 |
| [`brooks-sweep`](backend/.agents/skills/brooks-sweep/SKILL.md) | 综合检查代码、架构、技术债和测试质量，并按风险执行修复。 |
| [`brooks-test`](backend/.agents/skills/brooks-test/SKILL.md) | 评审测试脆弱性、过度 Mock、覆盖率假象、速度和可读性。 |
| [`build-graph`](backend/.agents/skills/build-graph/SKILL.md) | 建立或更新代码审查知识图谱，为导航和影响分析提供基础。 |
| [`code-review`](backend/.agents/skills/code-review/SKILL.md) | 从仓库规范和原始需求两个维度审查指定基线以来的变更。 |
| [`cso`](backend/.agents/skills/cso/SKILL.md) / [`gstack-cso`](backend/.agents/skills/gstack-cso/SKILL.md) | 执行安全审计；符合条件的项目可进一步验证问题并生成修复候选。 |
| [`debug-issue`](backend/.agents/skills/debug-issue/SKILL.md) | 结合代码知识图谱定位问题、追踪调用关系并分析原因。 |
| [`diagnosing-bugs`](backend/.agents/skills/diagnosing-bugs/SKILL.md) | 通过假设、证据和验证循环排查复杂错误与性能回退。 |
| [`everything-claude-code`](backend/.agents/skills/everything-claude-code/SKILL.md) | 提供 everything-claude-code 项目的 JavaScript 开发约定和提交规范。 |
| [`explore-codebase`](backend/.agents/skills/explore-codebase/SKILL.md) | 通过知识图谱理解代码结构、模块关系和关键实现。 |
| [`gstack-health`](backend/.agents/skills/gstack-health/SKILL.md) | 运行项目现有类型检查、Lint、测试等工具，汇总代码质量评分与趋势。 |
| [`gstack-investigate`](backend/.agents/skills/gstack-investigate/SKILL.md) | 按调查、分析、假设和实现阶段排查问题，先确认根因再修复。 |
| [`gstack-plan-devex-review`](backend/.agents/skills/gstack-plan-devex-review/SKILL.md) | 评审 API、CLI、SDK、文档和平台的开发者体验与接入流程。 |
| [`gstack-review`](backend/.agents/skills/gstack-review/SKILL.md) | 合入前审查代码差异，检查 SQL 安全、LLM 信任边界和条件副作用。 |
| [`health`](backend/.agents/skills/health/SKILL.md) / [`gstack-health`](backend/.agents/skills/gstack-health/SKILL.md) | 运行项目现有类型检查、Lint、测试等工具，汇总代码质量评分与趋势。 |
| [`implement`](backend/.agents/skills/implement/SKILL.md) | 按已有规格或任务单实现工作项。 |
| [`implement-spec`](backend/.agents/skills/implement-spec/SKILL.md) | 将明确的规格说明落实为代码。 |
| [`investigate`](backend/.agents/skills/investigate/SKILL.md) / [`gstack-investigate`](backend/.agents/skills/gstack-investigate/SKILL.md) | 按调查、分析、假设和实现阶段排查问题，先确认根因再修复。 |
| [`kent-beck-style`](backend/.agents/skills/kent-beck-style/SKILL.md) | 按简单设计与渐进重构原则检查代码异味，改善可读性。 |
| [`mcp-builder`](backend/.agents/skills/mcp-builder/SKILL.md) | 开发 Python 或 Node/TypeScript MCP 服务，封装外部 API 和工具。 |
| [`migrate-to-shoehorn`](backend/.agents/skills/migrate-to-shoehorn/SKILL.md) | 在测试中用 @total-typescript/shoehorn 替换类型断言，构建部分测试数据。 |
| [`plan-devex-review`](backend/.agents/skills/plan-devex-review/SKILL.md) / [`gstack-plan-devex-review`](backend/.agents/skills/gstack-plan-devex-review/SKILL.md) | 评审 API、CLI、SDK、文档和平台的开发者体验与接入流程。 |
| [`refactor-safely`](backend/.agents/skills/refactor-safely/SKILL.md) | 结合依赖分析和影响范围，规划并执行安全重构。 |
| [`review`](backend/.agents/skills/review/SKILL.md) / [`gstack-review`](backend/.agents/skills/gstack-review/SKILL.md) | 合入前审查代码差异，检查 SQL 安全、LLM 信任边界和条件副作用。 |
| [`review-changes`](backend/.agents/skills/review-changes/SKILL.md) | 结合变更检测和影响范围开展结构化代码审查。 |
| [`review-delta`](backend/.agents/skills/review-delta/SKILL.md) | 仅审查最近提交后的增量变更，并分析关联影响。 |
| [`review-pr`](backend/.agents/skills/review-pr/SKILL.md) | 结合知识图谱审查 PR 或分支差异，说明影响范围。 |
| [`security-review`](backend/.agents/skills/security-review/SKILL.md) | 检查认证授权、注入、XSS、SSRF、路径遍历和敏感信息泄露等漏洞。 |
| [`setup-pre-commit`](backend/.agents/skills/setup-pre-commit/SKILL.md) | 配置 Husky、lint-staged、格式化、类型检查和提交前测试。 |
| [`tdd`](backend/.agents/skills/tdd/SKILL.md) | 采用红灯、绿灯、重构循环开发功能或修复缺陷，支持集成测试。 |
| [`troubleshoot`](backend/.agents/skills/troubleshoot/SKILL.md) | 通过系统化根因分析排查错误和异常行为。 |
| [`typesafe-ai`](backend/.agents/skills/typesafe-ai/SKILL.md) | 使用 TypeSafe 将分类、路由、排序和验证等 AI 判断集成到程序。 |
| [`warden`](backend/.agents/skills/warden/SKILL.md) | 运行 Warden 分析提交前的代码变更，并配置审查规则和触发器。 |
| [`warden-sweep`](backend/.agents/skills/warden-sweep/SKILL.md) | 用 Warden 扫描整个代码库，核实发现的问题，并为有效问题创建草稿 PR。 |

<a id="test"></a>

## 功能测试与验证（test）

Web/iOS 功能验证、浏览器测试、性能回归、视觉检查和测试质量。

目录：[`test/.agents/skills/`](test/.agents/skills/) · 33 个技能入口。

| 技能 | 概要简介 |
| --- | --- |
| [`benchmark`](test/.agents/skills/benchmark/SKILL.md) / [`gstack-benchmark`](test/.agents/skills/gstack-benchmark/SKILL.md) | 建立网页加载、Web Vitals 和资源大小基线，检测性能回归。 |
| [`brooks-health`](test/.agents/skills/brooks-health/SKILL.md) | 从代码审查、架构、技术债和测试质量四个维度评估代码库。 |
| [`brooks-test`](test/.agents/skills/brooks-test/SKILL.md) | 评审测试脆弱性、过度 Mock、覆盖率假象、速度和可读性。 |
| [`browse`](test/.agents/skills/browse/SKILL.md) / [`gstack-browse`](test/.agents/skills/gstack-browse/SKILL.md) | 操控真实浏览器验证页面和用户流程，截图并检查控制台错误。 |
| [`browser-act`](test/.agents/skills/browser-act/SKILL.md) | 通过浏览器自动化完成表单、交互、截图、页面提取与网络请求捕获。 |
| [`browser-skill`](test/.agents/skills/browser-skill/SKILL.md) | 通过 bsk CLI 和扩展操作用户已登录的 Chromium，测试页面和调试网站。 |
| [`browser-use`](test/.agents/skills/browser-use/SKILL.md) | 通过 CDP 控制浏览器，执行交互、抓取、截图和应用测试。 |
| [`canary`](test/.agents/skills/canary/SKILL.md) / [`gstack-canary`](test/.agents/skills/gstack-canary/SKILL.md) | 部署后监控页面故障、控制台错误和性能回退。 |
| [`confidence-check`](test/.agents/skills/confidence-check/SKILL.md) | 实现前核对需求、重复实现、架构、官方资料和根因等准备条件。 |
| [`design-review`](test/.agents/skills/design-review/SKILL.md) / [`gstack-design-review`](test/.agents/skills/gstack-design-review/SKILL.md) | 检查并修复视觉层级、间距、一致性、交互和模板化设计问题。 |
| [`devex-review`](test/.agents/skills/devex-review/SKILL.md) / [`gstack-devex-review`](test/.agents/skills/gstack-devex-review/SKILL.md) | 实际尝试文档、接入与 CLI 流程，评估开发者体验并记录证据。 |
| [`ego-browser`](test/.agents/skills/ego-browser/SKILL.md) | 使用 ego 浏览器及已有登录会话进行网页操作、测试和质量检查。 |
| [`gstack-health`](test/.agents/skills/gstack-health/SKILL.md) | 运行项目现有类型检查、Lint、测试等工具，汇总代码质量评分与趋势。 |
| [`gstack-ios-design-review`](test/.agents/skills/gstack-ios-design-review/SKILL.md) | 在真实 iPhone 上检查视觉设计、Apple HIG 和界面一致性。 |
| [`gstack-ios-fix`](test/.agents/skills/gstack-ios-fix/SKILL.md) | 针对 iOS 测试发现的问题执行修复、重建、部署和真机验证。 |
| [`gstack-ios-qa`](test/.agents/skills/gstack-ios-qa/SKILL.md) | 通过调试桥在真实 iPhone 上执行截图、交互和状态验证。 |
| [`gstack-qa`](test/.agents/skills/gstack-qa/SKILL.md) | 系统测试 Web 应用，修复发现的问题并重新验证。 |
| [`gstack-qa-only`](test/.agents/skills/gstack-qa-only/SKILL.md) | 仅测试并报告 Web 应用问题，提供截图和复现步骤。 |
| [`gstack-setup-browser-cookies`](test/.agents/skills/gstack-setup-browser-cookies/SKILL.md) | 从用户 Chromium 浏览器导入选定站点 Cookie，用于已登录页面测试。 |
| [`health`](test/.agents/skills/health/SKILL.md) / [`gstack-health`](test/.agents/skills/gstack-health/SKILL.md) | 运行项目现有类型检查、Lint、测试等工具，汇总代码质量评分与趋势。 |
| [`ios-design-review`](test/.agents/skills/ios-design-review/SKILL.md) / [`gstack-ios-design-review`](test/.agents/skills/gstack-ios-design-review/SKILL.md) | 在真实 iPhone 上检查视觉设计、Apple HIG 和界面一致性。 |
| [`ios-fix`](test/.agents/skills/ios-fix/SKILL.md) / [`gstack-ios-fix`](test/.agents/skills/gstack-ios-fix/SKILL.md) | 针对 iOS 测试发现的问题执行修复、重建、部署和真机验证。 |
| [`ios-qa`](test/.agents/skills/ios-qa/SKILL.md) / [`gstack-ios-qa`](test/.agents/skills/gstack-ios-qa/SKILL.md) | 通过调试桥在真实 iPhone 上执行截图、交互和状态验证。 |
| [`migrate-to-shoehorn`](test/.agents/skills/migrate-to-shoehorn/SKILL.md) | 在测试中用 @total-typescript/shoehorn 替换类型断言，构建部分测试数据。 |
| [`qa`](test/.agents/skills/qa/SKILL.md) / [`gstack-qa`](test/.agents/skills/gstack-qa/SKILL.md) | 系统测试 Web 应用，修复发现的问题并重新验证。 |
| [`qa-only`](test/.agents/skills/qa-only/SKILL.md) / [`gstack-qa-only`](test/.agents/skills/gstack-qa-only/SKILL.md) | 仅测试并报告 Web 应用问题，提供截图和复现步骤。 |
| [`setup-browser-cookies`](test/.agents/skills/setup-browser-cookies/SKILL.md) / [`gstack-setup-browser-cookies`](test/.agents/skills/gstack-setup-browser-cookies/SKILL.md) | 从用户 Chromium 浏览器导入选定站点 Cookie，用于已登录页面测试。 |
| [`tdd`](test/.agents/skills/tdd/SKILL.md) | 采用红灯、绿灯、重构循环开发功能或修复缺陷，支持集成测试。 |

<a id="video"></a>

## 视频制作（video）

HTML 视频、程序化动画、AI 视频生成、宣传片复刻与剪辑。

目录：[`video/.agents/skills/`](video/.agents/skills/) · 13 个技能入口。

| 技能 | 概要简介 |
| --- | --- |
| [`answer-me-with-html`](video/.agents/skills/answer-me-with-html/SKILL.md) | 将说明整理为可视化 HTML 页面，也支持讲解视频生成。 |
| [`gsap`](video/.agents/skills/gsap/SKILL.md) | 提供 GSAP 动画、缓动、时间线和性能参考，主要服务 HyperFrames 动画。 |
| [`huashu-design`](video/.agents/skills/huashu-design/SKILL.md) | 以多方向方案探索制作高保真 HTML 原型、演示、动画和可视化。 |
| [`hyperframes`](video/.agents/skills/hyperframes/SKILL.md) | 制作 HTML 视频合成、动画、字幕、配音、音频响应效果和转场。 |
| [`hyperframes-cli`](video/.agents/skills/hyperframes-cli/SKILL.md) | 使用 HyperFrames CLI 初始化、检查、预览、渲染、转录和生成配音。 |
| [`hyperframes-registry`](video/.agents/skills/hyperframes-registry/SKILL.md) | 安装并接入 HyperFrames 的视频组件和子合成模块。 |
| [`remotion-best-practices`](video/.agents/skills/remotion-best-practices/SKILL.md) | 路由到 Remotion 创作、字幕、多媒体、预览和渲染等配套技能。 |
| [`seedance-20`](video/.agents/skills/seedance-20/SKILL.md) | 为 Seedance 2.0 设计视频提示词、参考素材、首尾帧、对话和生成流程。 |
| [`seedance2-skill`](video/.agents/skills/seedance2-skill/SKILL.md) | 围绕即梦 Seedance 完成创意扩写、运镜、验证和视频 API 生成。 |
| [`video-copy`](video/.agents/skills/video-copy/SKILL.md) | 分析参考宣传片，结合新产品信息生成分镜、素材和视频片段。 |
| [`video-use`](video/.agents/skills/video-use/SKILL.md) | 通过对话完成视频转录、剪切、调色、动画叠加和字幕烧录。 |
| [`website-to-hyperframes`](video/.agents/skills/website-to-hyperframes/SKILL.md) | 采集网站画面并制作宣传片、产品导览或社交广告视频。 |
| [`yichen-jianying-edit`](video/.agents/skills/yichen-jianying-edit/SKILL.md) | 在匹配版本的剪映环境中生成或修改可编辑草稿，并按需导出 MP4。 |

<a id="article"></a>

## 文章与文档（article）

文章构思、技术博客、项目文档维护和 PDF 导出。

目录：[`article/.agents/skills/`](article/.agents/skills/) · 10 个技能入口。

| 技能 | 概要简介 |
| --- | --- |
| [`distill-worklog-to-blog`](article/.agents/skills/distill-worklog-to-blog/SKILL.md) | 把工作记录、调试和项目经验整理为脱敏的中文技术博客及配图。 |
| [`document-generate`](article/.agents/skills/document-generate/SKILL.md) / [`gstack-document-generate`](article/.agents/skills/gstack-document-generate/SKILL.md) | 按教程、操作指南、参考和解释四类结构生成缺失的项目文档。 |
| [`document-release`](article/.agents/skills/document-release/SKILL.md) / [`gstack-document-release`](article/.agents/skills/gstack-document-release/SKILL.md) | 根据已交付变更更新项目文档、变更日志和待办记录。 |
| [`gstack-make-pdf`](article/.agents/skills/gstack-make-pdf/SKILL.md) | 将 Markdown 排版为带页码、目录和合理分页的 PDF 文档。 |
| [`make-pdf`](article/.agents/skills/make-pdf/SKILL.md) / [`gstack-make-pdf`](article/.agents/skills/gstack-make-pdf/SKILL.md) | 将 Markdown 排版为带页码、目录和合理分页的 PDF 文档。 |
| [`writing-beats`](article/.agents/skills/writing-beats/SKILL.md) | 把已有素材组织为叙事节奏，逐步铺垫概念和论点。 |
| [`writing-fragments`](article/.agents/skills/writing-fragments/SKILL.md) | 探索和积累原始写作片段，暂不强求文章结构。 |
| [`writing-shape`](article/.agents/skills/writing-shape/SKILL.md) | 把零散素材按段落组织成结构连贯的文章。 |

<a id="browser"></a>

## 浏览器与采集（browser）

平台内容读取、浏览器连接、网页采集和桌面应用操作。

目录：[`browser/.agents/skills/`](browser/.agents/skills/) · 11 个技能入口。

| 技能 | 概要简介 |
| --- | --- |
| [`agent-reach`](browser/.agents/skills/agent-reach/SKILL.md) | 只读搜索和读取社交、视频等平台内容，补充正文、评论和字幕获取能力。 |
| [`computer-use`](browser/.agents/skills/computer-use/SKILL.md) | 通过本机 GUI 操作原生应用或外部浏览器，读取界面、点击、输入和截图。 |
| [`connect-chrome`](browser/.agents/skills/connect-chrome/SKILL.md) | 启动可供 AI 控制的 GStack Chromium 浏览器。 |
| [`gstack-open-gstack-browser`](browser/.agents/skills/gstack-open-gstack-browser/SKILL.md) | 启动带侧栏扩展的可视 GStack 浏览器，实时观察浏览器操作。 |
| [`gstack-pair-agent`](browser/.agents/skills/gstack-pair-agent/SKILL.md) | 为远程 AI Agent 配对并开放浏览器访问。 |
| [`gstack-scrape`](browser/.agents/skills/gstack-scrape/SKILL.md) | 通过已有登录会话只读提取网页数据，并返回 JSON。 |
| [`gstack-skillify`](browser/.agents/skills/gstack-skillify/SKILL.md) | 把成功的网页采集过程固化为可复用的技能、脚本和测试。 |
| [`open-gstack-browser`](browser/.agents/skills/open-gstack-browser/SKILL.md) / [`gstack-open-gstack-browser`](browser/.agents/skills/gstack-open-gstack-browser/SKILL.md) | 启动带侧栏扩展的可视 GStack 浏览器，实时观察浏览器操作。 |
| [`pair-agent`](browser/.agents/skills/pair-agent/SKILL.md) / [`gstack-pair-agent`](browser/.agents/skills/gstack-pair-agent/SKILL.md) | 为远程 AI Agent 配对并开放浏览器访问。 |
| [`scrape`](browser/.agents/skills/scrape/SKILL.md) / [`gstack-scrape`](browser/.agents/skills/gstack-scrape/SKILL.md) | 通过已有登录会话只读提取网页数据，并返回 JSON。 |
| [`skillify`](browser/.agents/skills/skillify/SKILL.md) / [`gstack-skillify`](browser/.agents/skills/gstack-skillify/SKILL.md) | 把成功的网页采集过程固化为可复用的技能、脚本和测试。 |

<a id="research"></a>

## 搜索与研究（research）

实时检索、系统研究和多 AI 平台结果比较。

目录：[`research/.agents/skills/`](research/.agents/skills/) · 3 个技能入口。

| 技能 | 概要简介 |
| --- | --- |
| [`anysearch`](research/.agents/skills/anysearch/SKILL.md) | 执行实时网页与垂直搜索，支持并行批量检索和 URL 正文提取。 |
| [`deep-research`](research/.agents/skills/deep-research/SKILL.md) | 围绕研究问题开展系统调查，提供来源引用和综合结论。 |
| [`multi-ai-platform-research`](research/.agents/skills/multi-ai-platform-research/SKILL.md) | 跨多个 AI 聊天平台研究、比较并综合答案。 |

<a id="finance"></a>

## 股票与金融（finance）

A 股分析、金融数据查询、概念事件归档和雪球访问配置。

目录：[`finance/.agents/skills/`](finance/.agents/skills/) · 4 个技能入口。

| 技能 | 概要简介 |
| --- | --- |
| [`ashare-stock-analysis`](finance/.agents/skills/ashare-stock-analysis/SKILL.md) | 根据 A 股代码或名称生成中文个股投研分析报告。 |
| [`ifind-data`](finance/.agents/skills/ifind-data/SKILL.md) | 通过同花顺 iFind 查询行情、财务、基金、指数和选股数据。 |
| [`save-concept-events`](finance/.agents/skills/save-concept-events/SKILL.md) | 将股票概念、主题事件、催化因素和股票清单保存到概念库。 |
| [`update-xueqiu-cookie`](finance/.agents/skills/update-xueqiu-cookie/SKILL.md) | 更新股票数据管理工具所使用的雪球 Cookie。 |

<a id="agent"></a>

## 智能体与协作（agent）

Agent 管理、模型第二意见、模型比较、团队知识与上下文管理。

目录：[`agent/.agents/skills/`](agent/.agents/skills/) · 14 个技能入口。

| 技能 | 概要简介 |
| --- | --- |
| [`autoclaw-fleet`](agent/.agents/skills/autoclaw-fleet/SKILL.md) | 管理 Windows 上的 OpenClaw/AutoClaw 实例，执行任务、部署应用并查询运行状态。 |
| [`benchmark-models`](agent/.agents/skills/benchmark-models/SKILL.md) / [`gstack-benchmark-models`](agent/.agents/skills/gstack-benchmark-models/SKILL.md) | 对比不同模型执行同一技能时的耗时、Token、成本及可选质量评分。 |
| [`codex`](agent/.agents/skills/codex/SKILL.md) | 通过 OpenAI Codex CLI 获取代码审查、独立意见和对抗性检查。 |
| [`gstack-claude-code`](agent/.agents/skills/gstack-claude-code/SKILL.md) | 调用 Claude Code CLI，对代码变更进行审查、挑战或咨询。 |
| [`gstack-learn`](agent/.agents/skills/gstack-learn/SKILL.md) | 搜索、整理、清理并导出项目中积累的经验。 |
| [`gstack-setup-gbrain`](agent/.agents/skills/gstack-setup-gbrain/SKILL.md) | 安装并初始化 gbrain，配置知识存储、MCP 和信任策略。 |
| [`gstack-sync-gbrain`](agent/.agents/skills/gstack-sync-gbrain/SKILL.md) | 同步代码到 gbrain，并刷新 Agent 使用知识搜索的项目指引。 |
| [`learn`](agent/.agents/skills/learn/SKILL.md) / [`gstack-learn`](agent/.agents/skills/gstack-learn/SKILL.md) | 搜索、整理、清理并导出项目中积累的经验。 |
| [`setup-gbrain`](agent/.agents/skills/setup-gbrain/SKILL.md) / [`gstack-setup-gbrain`](agent/.agents/skills/gstack-setup-gbrain/SKILL.md) | 安装并初始化 gbrain，配置知识存储、MCP 和信任策略。 |
| [`sync-gbrain`](agent/.agents/skills/sync-gbrain/SKILL.md) / [`gstack-sync-gbrain`](agent/.agents/skills/gstack-sync-gbrain/SKILL.md) | 同步代码到 gbrain，并刷新 Agent 使用知识搜索的项目指引。 |
| [`teamai`](agent/.agents/skills/teamai/SKILL.md) | 同步团队共享的技能、规则、文档和配置，并管理团队代码知识库。 |
| [`token-efficiency`](agent/.agents/skills/token-efficiency/SKILL.md) | 切换到精简表达模式，降低上下文和输出的 Token 消耗。 |
| [`writing-for-agents`](agent/.agents/skills/writing-for-agents/SKILL.md) | 编写面向 Agent 的文档、技能说明和 AGENTS.md / CLAUDE.md。 |

<a id="mobile"></a>

## 移动端工具（mobile）

iOS 调试桥清理与同步；iOS 测试和视觉审查技能另见 test 分类。

目录：[`mobile/.agents/skills/`](mobile/.agents/skills/) · 4 个技能入口。

| 技能 | 概要简介 |
| --- | --- |
| [`gstack-ios-clean`](mobile/.agents/skills/gstack-ios-clean/SKILL.md) | 移除 iOS DebugBridge 包及其调试接入代码。 |
| [`gstack-ios-sync`](mobile/.agents/skills/gstack-ios-sync/SKILL.md) | 根据最新模板同步 iOS 调试桥、状态访问器和相关接入代码。 |
| [`ios-clean`](mobile/.agents/skills/ios-clean/SKILL.md) / [`gstack-ios-clean`](mobile/.agents/skills/gstack-ios-clean/SKILL.md) | 移除 iOS DebugBridge 包及其调试接入代码。 |
| [`ios-sync`](mobile/.agents/skills/ios-sync/SKILL.md) / [`gstack-ios-sync`](mobile/.agents/skills/gstack-ios-sync/SKILL.md) | 根据最新模板同步 iOS 调试桥、状态访问器和相关接入代码。 |

<a id="knowledge"></a>

## 知识与教学（knowledge）

网页笔记归档、学习引导和课程练习目录生成。

目录：[`knowledge/.agents/skills/`](knowledge/.agents/skills/) · 3 个技能入口。

| 技能 | 概要简介 |
| --- | --- |
| [`save-notes`](knowledge/.agents/skills/save-notes/SKILL.md) | 提取网页或文章内容，生成结构化 Markdown 笔记并归档。 |
| [`scaffold-exercises`](knowledge/.agents/skills/scaffold-exercises/SKILL.md) | 生成包含章节、题目、答案和解释的课程练习目录。 |
| [`teach`](knowledge/.agents/skills/teach/SKILL.md) | 结合当前工作区，引导学习技能或概念并记录学习过程。 |

<a id="reverse"></a>

## 逆向工程（reverse）

基于发布产物和运行证据的逆向分析，以及专项技能路由。

目录：[`reverse/.agents/skills/`](reverse/.agents/skills/) · 2 个技能入口。

| 技能 | 概要简介 |
| --- | --- |
| [`reverse-engineer-anything`](reverse/.agents/skills/reverse-engineer-anything/SKILL.md) | 基于原生、托管、Electron 等发布产物及运行证据进行逆向分析。 |
| [`reverse-skill`](reverse/.agents/skills/reverse-skill/SKILL.md) | 为逆向工程、安全测试、移动端、固件等任务选择相应专项技能。 |

<a id="tooling"></a>

## 工具与配置（tooling）

技能路由、方案质询、操作保护、编辑范围和工具升级。

目录：[`tooling/.agents/skills/`](tooling/.agents/skills/) · 16 个技能入口。

| 技能 | 概要简介 |
| --- | --- |
| [`_gstack-command`](tooling/.agents/skills/_gstack-command/SKILL.md) | 根据请求选择合适的 gstack 技能入口。 |
| [`ask-matt`](tooling/.agents/skills/ask-matt/SKILL.md) | 根据当前场景推荐适合的技能或工作流程。 |
| [`careful`](tooling/.agents/skills/careful/SKILL.md) / [`gstack-careful`](tooling/.agents/skills/gstack-careful/SKILL.md) | 在删除、强制推送等破坏性操作前增加保护检查。 |
| [`freeze`](tooling/.agents/skills/freeze/SKILL.md) / [`gstack-freeze`](tooling/.agents/skills/gstack-freeze/SKILL.md) | 限制当前会话的文件修改范围到指定目录。 |
| [`grill-with-files`](tooling/.agents/skills/grill-with-files/SKILL.md) | 结合实际文件检验计划，用文件证据澄清问题和实施假设。 |
| [`gstack`](tooling/.agents/skills/gstack/SKILL.md) | 路由到规划、审查、测试、发布、调试、文档和设计等 gstack 技能。 |
| [`gstack-guard`](tooling/.agents/skills/gstack-guard/SKILL.md) | 组合破坏性命令保护与目录编辑范围限制。 |
| [`gstack-plan-tune`](tooling/.agents/skills/gstack-plan-tune/SKILL.md) | 配置 gstack 提问频率、问题偏好和开发者交互画像。 |
| [`gstack-unfreeze`](tooling/.agents/skills/gstack-unfreeze/SKILL.md) | 解除此前设置的目录编辑限制。 |
| [`gstack-upgrade`](tooling/.agents/skills/gstack-upgrade/SKILL.md) | 检测安装方式并将 gstack 升级到最新版本。 |
| [`guard`](tooling/.agents/skills/guard/SKILL.md) / [`gstack-guard`](tooling/.agents/skills/gstack-guard/SKILL.md) | 组合破坏性命令保护与目录编辑范围限制。 |
| [`plan-tune`](tooling/.agents/skills/plan-tune/SKILL.md) / [`gstack-plan-tune`](tooling/.agents/skills/gstack-plan-tune/SKILL.md) | 配置 gstack 提问频率、问题偏好和开发者交互画像。 |
| [`unfreeze`](tooling/.agents/skills/unfreeze/SKILL.md) / [`gstack-unfreeze`](tooling/.agents/skills/gstack-unfreeze/SKILL.md) | 解除此前设置的目录编辑限制。 |
| [`wait-what`](tooling/.agents/skills/wait-what/SKILL.md) | 重新组织并解释上一条未被理解的回答。 |

<a id="lark"></a>

## 飞书集成（lark）

飞书消息、文档、表格、日程、会议、审批、任务和应用开发。

目录：[`lark/.agents/skills/`](lark/.agents/skills/) · 27 个技能入口。

| 技能 | 概要简介 |
| --- | --- |
| [`lark-approval`](lark/.agents/skills/lark-approval/SKILL.md) | 查询和处理审批任务，搜索审批定义并发起原生审批。 |
| [`lark-apps`](lark/.agents/skills/lark-apps/SKILL.md) | 开发、设计、部署和管理妙搭应用，查询运行数据并配置自动化。 |
| [`lark-attendance`](lark/.agents/skills/lark-attendance/SKILL.md) | 查询当前用户的考勤打卡记录。 |
| [`lark-base`](lark/.agents/skills/lark-base/SKILL.md) | 操作多维表格的表、字段、记录、视图、仪表盘、应用模式和工作流。 |
| [`lark-calendar`](lark/.agents/skills/lark-calendar/SKILL.md) | 查询和管理日历、日程、参会人、忙闲与会议室预订。 |
| [`lark-contact`](lark/.agents/skills/lark-contact/SKILL.md) | 按姓名或邮箱查找人员，查询联系方式及可见机器人。 |
| [`lark-doc`](lark/.agents/skills/lark-doc/SKILL.md) | 读取、创建和编辑云文档，处理图片、附件及思维笔记。 |
| [`lark-drive`](lark/.agents/skills/lark-drive/SKILL.md) | 管理云空间文件、文件夹、导入导出、权限、评论和版本。 |
| [`lark-event`](lark/.agents/skills/lark-event/SKILL.md) | 订阅和消费飞书实时事件，支持有界运行和 NDJSON 输出。 |
| [`lark-im`](lark/.agents/skills/lark-im/SKILL.md) | 收发和搜索消息，管理群聊、文件、交互卡片及卡片回调。 |
| [`lark-mail`](lark/.agents/skills/lark-mail/SKILL.md) | 查询、起草、发送和管理邮件，以及邮件标签、文件夹和规则。 |
| [`lark-markdown`](lark/.agents/skills/lark-markdown/SKILL.md) | 创建、读取、上传、编辑和比较飞书 Markdown 文件。 |
| [`lark-minutes`](lark/.agents/skills/lark-minutes/SKILL.md) | 搜索妙记，管理音视频、转写产物、说话人及查看权限。 |
| [`lark-note`](lark/.agents/skills/lark-note/SKILL.md) | 在已知 note_id 时读取会议纪要详情、关联文档和原始逐字记录。 |
| [`lark-okr`](lark/.agents/skills/lark-okr/SKILL.md) | 查看与管理 OKR 周期、目标、关键结果、对齐关系和进展。 |
| [`lark-openapi-explorer`](lark/.agents/skills/lark-openapi-explorer/SKILL.md) | 从官方文档发现 CLI 尚未封装的飞书原生 OpenAPI。 |
| [`lark-shared`](lark/.agents/skills/lark-shared/SKILL.md) | 配置 lark-cli 登录、身份、授权范围与权限问题。 |
| [`lark-sheets`](lark/.agents/skills/lark-sheets/SKILL.md) | 编辑电子表格、公式、样式、图表、透视表和数据分析模型。 |
| [`lark-skill-maker`](lark/.agents/skills/lark-skill-maker/SKILL.md) | 将飞书 API 操作或多步流程封装为可复用技能。 |
| [`lark-slides`](lark/.agents/skills/lark-slides/SKILL.md) | 创建和编辑飞书原生幻灯片及单个页面。 |
| [`lark-task`](lark/.agents/skills/lark-task/SKILL.md) | 管理任务、清单、子任务、协作成员、附件和任务智能体。 |
| [`lark-vc`](lark/.agents/skills/lark-vc/SKILL.md) | 查询进行中和历史视频会议，读取会中内容、纪要与参会人快照。 |
| [`lark-vc-agent`](lark/.agents/skills/lark-vc-agent/SKILL.md) | 让应用机器人加入或离开会议，读取事件并发送会中消息或表情。 |
| [`lark-whiteboard`](lark/.agents/skills/lark-whiteboard/SKILL.md) | 读取、编辑和导出云文档中的画板。 |
| [`lark-wiki`](lark/.agents/skills/lark-wiki/SKILL.md) | 管理知识空间、成员和文档节点层级。 |
| [`lark-workflow-meeting-summary`](lark/.agents/skills/lark-workflow-meeting-summary/SKILL.md) | 汇总指定时间范围的会议纪要，生成结构化报告。 |
| [`lark-workflow-standup-report`](lark/.agents/skills/lark-workflow-standup-report/SKILL.md) | 结合日历与未完成任务，生成指定日期的安排摘要。 |

## 维护说明

新增或调整分类后，同步更新分类总览的数量和对应简介表格。修改技能前请阅读其说明；跨分类的同名目录是独立副本，需要按实际需求同步维护。
