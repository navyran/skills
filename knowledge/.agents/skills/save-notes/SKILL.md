---
name: save-notes
description: 智能笔记保存工具，从网页/文章链接提取内容，生成结构化Markdown笔记，自动保存到 memory/notes/ 目录并提交Git版本控制。
read_when:
  - 用户说"保存笔记"、"保存这篇文章"、"整理这篇"
  - 用户提供文章链接并要求保存
  - 需要将网页内容整理为笔记并归档
  - 需要将内容保存为 Markdown 文件并提交 Git
metadata:
  emoji: 📝
  category: 笔记管理
  author: OpenClaw AI
  version: 2.0.0
  requires:
    bins: [node]
    skills: [agent-browser]
allowed-tools:
  - Bash(save-notes:*)
---

# 智能笔记保存 Skill

## 功能特性
1. **网页内容提取**：使用 agent-browser 自动从 URL 获取文章内容
2. **结构化保存**：保存为格式良好的 Markdown 文件到 `memory/notes/` 目录
3. **自动 Git 操作**：自动添加并提交到 Git 仓库
4. **统一命名规范**：自动生成符合规范的文件名

## 触发场景

**当用户说以下内容时必须调用此 skill：**
- "保存这篇文章的笔记"
- "把这篇文章整理到笔记里"
- "保存这个链接的内容"
- "帮我归档这篇文章"
- 任何包含"保存笔记"、"保存文章"、"整理到笔记"等关键词的请求

## 使用方法

### 标准调用
```bash
node skills/save-notes/scripts/save-notes.js <文章URL> <笔记标题>
```

### 示例
```bash
node skills/save-notes/scripts/save-notes.js "https://example.com/article" "文章标题"
```

## 工作流程

1. **接收参数**：文章 URL + 笔记标题
2. **提取内容**：使用 agent-browser 打开网页并提取文本内容
3. **生成笔记**：使用模板生成结构化 Markdown 文件
4. **保存文件**：保存到 `memory/notes/` 目录
5. **Git 提交**：自动 `git add` + `git commit`

## 保存路径配置

- **默认路径**：`~/PycharmProjects/docs/`
- **文件命名**：`{英文标题}.md`（自动清理非法字符）

## 输出结构

生成的 Markdown 笔记包含：
- 标题
- 基本信息（来源、作者、日期、保存时间）
- 核心内容
- 关键要点
- 标签

## 依赖要求

- agent-browser skill（用于网页内容提取）
- Git（用于版本控制）
- Node.js（运行脚本）

## 注意事项

⚠️ **重要：保存笔记时必须调用此 skill，禁止直接使用 write 工具写入 memory 目录！**

当用户要求保存文章/笔记时：
1. 先调用此 skill 脚本处理
2. 不要直接写文件到 memory/notes/
3. 确保 Git 提交正确完成

## 版本历史

- v2.0.0：完全重写，支持 agent-browser 提取内容，修复路径配置
- v1.0.0：初始版本
