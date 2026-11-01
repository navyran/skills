# 流程图图片化规范

## 发布规则

Mermaid 只作为中间关系草图，不作为博客最终交付物。文章主体完成后，扫描全部 Mermaid 代码块，逐张生成 PNG 或 WebP 信息图并替换。

图像生成不可用、中文标签错误或流程方向错误时，不得降级保留 Mermaid。先减少图中文字、拆分过于复杂的图，再重新生成。

## 转换流程

### 1. 提取图的语义

从 Mermaid 或文字草图中整理：

- 图的核心结论。
- 节点和分组。
- 节点之间的方向。
- 循环、分支和人工门禁。
- 必须保留的中文标签。
- 可以交给正文解释、无需放进图片的细节。

先完成脱敏。不得将内部名称、地址、账号、任务标识和供应商信息交给图像生成工具。

### 2. 为每张图单独生成

使用可用的 imagegen Skill 或内置图像生成工具，每张流程图单独调用一次。使用 infographic-diagram 或 productivity-visual 类型，默认采用 16:9 横版。

提示词至少包含：

~~~text
Use case: infographic-diagram
Asset type: inline technical diagram for a Chinese blog
Primary request: <图的核心关系>
Style/medium: clean vector-like editorial infographic
Composition/framing: 16:9 landscape, clear directional flow
Text (verbatim): "<必须准确出现的中文标签>"
Constraints: exact labels only; no extra text; no logos; no watermark;
arrows must not cross text; generous spacing; high contrast
~~~

正文已经解释的细节不要重复塞入图片。优先使用 5–8 个短标签；标签过多时拆图或让正文承担解释。

### 3. 检查生成结果

逐张检查：

- 中文标签是否逐字正确且没有重复。
- 节点是否齐全。
- 箭头方向、循环和分支是否符合原意。
- 连线是否穿过节点或文字。
- 是否出现额外文字、品牌、人物或装饰性界面。
- 画幅和字号是否适合博客正文阅读。

若只有一个问题，使用单一目标重新生成或编辑；若文字错误较多，减少图片标签后重新生成，不在错误图上继续叠加内容。

### 4. 保存并替换

- 将最终图片复制到文章所在日期目录。
- 使用不含敏感信息的稳定英文文件名，例如 ai-regression-learning-loop.png。
- 保留生成工具的源文件，不覆盖无关同名图片。
- 将 Mermaid 代码块替换为相对图片引用和一句图注。

示例：

~~~markdown
![AI 自动化回归的经验沉淀闭环](./ai-regression-learning-loop.png)

*图：异常归因、方案修正、人工评审与独立复跑形成持续学习闭环。*
~~~

### 5. 发布前门禁

- 运行 validate_blog_post.py，Mermaid 残留必须导致校验失败。
- 确认每个本地图片链接可解析，文件非空且为 PNG/WebP。
- 再做一次图像语义检查，确保图片本身也已脱敏。
- 最终交付时列出文章和所有生成图片的绝对路径，并说明使用的生成模式和提示词摘要。
