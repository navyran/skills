# 保存笔记 Skill 使用指南

## 概述
这个skill允许OpenClaw AI助手自动从网页提取内容，生成结构化笔记，并保存到指定位置，支持自动git提交和推送。

## 在OpenClaw中集成

### 1. 技能识别
当用户请求保存文章或笔记时，识别以下关键词：
- "保存笔记"
- "保存文章"
- "整理这篇文章"
- "添加到知识库"
- "git保存"

### 2. 执行流程
以下是完整的执行流程：

```javascript
// 伪代码流程
async function saveNotesWorkflow(userRequest) {
  // 1. 解析用户请求
  const { url, savePath, category } = parseUserRequest(userRequest);
  
  // 2. 使用浏览器工具提取内容
  const articleContent = await extractWithBrowser(url);
  
  // 3. 生成结构化笔记
  const noteContent = generateStructuredNote(articleContent, url, category);
  
  // 4. 保存到文件系统
  const filePath = saveToFileSystem(noteContent, savePath);
  
  // 5. 自动git操作（如果配置了git）
  if (hasGitConfig(savePath)) {
    await gitCommitAndPush(filePath, savePath);
  }
  
  // 6. 返回结果给用户
  return formatResult(filePath, articleContent);
}
```

## 实际使用示例

### 示例1：简单保存
**用户输入**：
```
保存这篇文章的笔记：https://example.com/article
```

**助手响应**：
```
好的，我来帮你保存这篇文章的笔记。

🔍 正在提取文章内容...
📝 文章标题：如何有效进行向上管理
👤 作者：职场达人

📋 正在生成结构化笔记...
✅ 已分析出3个核心策略

💾 正在保存到默认位置：~/PycharmProjects/docs/
📄 文件名：如何有效进行向上管理_1773316699913.md

🔄 正在执行Git操作...
✅ 已提交并推送到远程仓库

🎉 完成！笔记已保存并同步。
```

### 示例2：指定位置保存
**用户输入**：
```
保存这篇文章到我的学习笔记文件夹：https://example.com/tech-article
```

**助手响应**：
```
好的，保存到你的学习笔记文件夹。

📁 目标位置：~/Documents/学习笔记/AI技术
🏷️  分类：技术学习

正在处理...
✅ 完成！笔记已保存到：~/Documents/学习笔记/AI技术/最新AI技术发展趋势.md
```

## 技能配置

### 环境变量配置
可以在OpenClaw配置中设置：
```bash
# 默认保存路径
export SAVE_NOTES_DEFAULT_PATH=~/知识库

# Git自动提交（true/false）
export SAVE_NOTES_GIT_AUTO=true

# 默认分类
export SAVE_NOTES_DEFAULT_CATEGORY=未分类
```

### 模板自定义
可以修改 `templates/note-template.md` 来自定义笔记格式：
```markdown
# {{title}}

## 基本信息
- 来源：{{url}}
- 保存时间：{{saveTime}}

## 内容摘要
{{summary}}

## 我的思考
<!-- 在这里添加个人见解 -->
```

## 错误处理

### 常见错误及处理
1. **URL访问失败**
   - 检查网络连接
   - 验证URL是否正确
   - 尝试使用备用浏览器配置

2. **内容提取失败**
   - 页面可能需要JavaScript
   - 尝试手动提取关键内容
   - 使用截图+OCR备用方案

3. **文件保存失败**
   - 检查目录权限
   - 验证磁盘空间
   - 确保文件名合法

4. **Git操作失败**
   - 检查git配置
   - 验证远程仓库权限
   - 处理合并冲突

### 优雅降级
如果某个步骤失败，提供替代方案：
- Git失败 → 仅保存本地文件
- 内容提取失败 → 提示用户手动输入
- 保存路径无效 → 使用临时位置

## 高级功能

### 批量处理
支持一次处理多个URL：
```
保存这些文章：
1. https://example.com/article1
2. https://example.com/article2
3. https://example.com/article3
```

### 智能分类
根据内容自动分类：
- 技术文章 → 技术学习
- 职场技巧 → 职场技能
- 投资理财 → 财务管理

### 内容增强
- 自动生成摘要
- 提取关键要点
- 生成思维导图
- 添加相关标签

## 性能优化

### 缓存策略
- 缓存已访问的URL
- 避免重复提取相同内容
- 增量更新已有笔记

### 异步处理
- 长时间操作使用后台任务
- 提供进度反馈
- 支持取消操作

## 监控和日志

### 日志记录
记录关键操作：
```json
{
  "timestamp": "2026-03-12T20:16:00Z",
  "operation": "save_notes",
  "url": "https://example.com/article",
  "save_path": "~/PycharmProjects/docs/职场",
  "status": "success",
  "file_size": 4364,
  "git_commit": "a5ae736"
}
```

### 性能指标
- 内容提取时间
- 文件保存时间
- Git操作时间
- 总体成功率

## 安全考虑

### 输入验证
- 验证URL格式
- 防止路径遍历攻击
- 限制文件大小

### 权限控制
- 检查文件系统权限
- 验证Git凭证
- 保护敏感信息

## 扩展建议

### 未来功能
1. **OCR支持** - 从图片提取文字
2. **语音转文字** - 保存语音内容
3. **多格式导出** - PDF、HTML、Word
4. **云同步** - 同步到云存储
5. **协作功能** - 共享笔记

### 集成其他工具
- 与Obsidian集成
- 与Notion API对接
- 与微信读书同步
- 与RSS阅读器整合

## 测试用例

### 单元测试
```bash
# 运行测试
cd ~/.openclaw/workspace/skills/save-notes
node test/test-skill.js
```

### 集成测试
测试完整流程：
1. 提供测试URL
2. 执行保存操作
3. 验证输出文件
4. 检查Git提交

## 故障排除

### 诊断命令
```bash
# 检查技能文件
ls -la ~/.openclaw/workspace/skills/save-notes/

# 测试脚本运行
node ~/.openclaw/workspace/skills/save-notes/scripts/save-notes.js --help

# 检查依赖
npm list --prefix ~/.openclaw/workspace/skills/save-notes/
```

### 常见问题
1. **脚本权限问题**
   ```bash
   chmod +x ~/.openclaw/workspace/skills/save-notes/scripts/*.js
   ```

2. **Node.js版本问题**
   ```bash
   node --version  # 需要Node.js 14+
   ```

3. **Git配置问题**
   ```bash
   git config --global user.email "you@example.com"
   git config --global user.name "Your Name"
   ```

## 总结

这个保存笔记Skill为OpenClaw提供了强大的内容保存和管理能力。通过自动化的工作流程，用户可以轻松地将有价值的网络内容保存到个人知识库，并享受版本控制的便利。

关键优势：
- ✅ 自动化程度高
- ✅ 支持Git版本控制
- ✅ 结构化笔记格式
- ✅ 灵活配置选项
- ✅ 良好的错误处理

通过合理配置和使用，这个skill可以显著提高知识管理的效率。