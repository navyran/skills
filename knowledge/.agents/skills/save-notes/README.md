# 保存笔记 Skill

一个智能的笔记保存工具，能够自动从网页提取内容，生成结构化笔记，并保存到指定位置，支持自动git提交和推送。

## 功能特点

### 🎯 核心功能
1. **网页内容提取** - 自动从URL获取文章内容
2. **智能分析** - 提取核心观点，生成思维导图
3. **结构化保存** - 保存为格式良好的Markdown文件
4. **自动git操作** - 自动提交和推送到git仓库
5. **灵活配置** - 支持自定义保存路径和git配置

### 📁 文件结构
```
save-notes/
├── SKILL.md          # 技能说明文档
├── README.md         # 详细使用说明
├── package.json      # 项目配置
├── scripts/
│   └── save-notes.js # 主要脚本
└── templates/
    └── note-template.md # 笔记模板
```

## 安装和使用

### 1. 基本使用
```bash
# 直接运行脚本
node scripts/save-notes.js <文章URL> <保存路径> [分类]
```

### 2. 在OpenClaw中使用
当用户请求保存文章笔记时，按照以下流程操作：

1. **获取文章URL**
2. **提取内容**（使用浏览器工具）
3. **分析内容**，生成结构化笔记
4. **保存到指定位置**
5. **自动git提交和推送**

### 3. 示例命令
```bash
# 保存文章到默认位置
node scripts/save-notes.js https://example.com/article ~/PycharmProjects/docs

# 保存文章到指定分类
node scripts/save-notes.js https://example.com/article ~/PycharmProjects/docs/职场 "职场技能"
```

## 配置选项

### 环境变量
```bash
# 默认保存路径
export SAVE_NOTES_PATH=~/my-notes

# 禁用自动git提交
export GIT_AUTO_COMMIT=false
```

### 配置文件
可以在脚本中修改`CONFIG`对象来自定义行为。

## 工作流程

### 步骤1：内容提取
- 使用浏览器工具访问URL
- 提取标题、作者、发布日期
- 获取文章正文内容
- 分析关键要点

### 步骤2：笔记生成
- 使用模板生成结构化Markdown
- 添加元数据（来源、时间、分类）
- 生成思维导图结构
- 添加个人思考区域

### 步骤3：文件保存
- 清理文件名（移除非法字符）
- 保存到指定目录
- 确保目录存在

### 步骤4：Git操作
- 检查是否为git仓库
- 添加文件到git
- 提交更改
- 推送到远程仓库
- 处理可能的冲突

## 集成到OpenClaw

### 作为Skill使用
1. 将本skill复制到OpenClaw的skills目录
2. 在需要时引用SKILL.md中的说明
3. 按照流程执行保存操作

### 示例对话
```
用户：保存这篇文章的笔记：https://example.com/article
助手：好的，我来帮你保存这篇文章的笔记...
      1. 正在提取文章内容...
      2. 正在生成结构化笔记...
      3. 正在保存到~/PycharmProjects/docs/职场...
      4. 正在执行git提交和推送...
      完成！笔记已保存到：~/PycharmProjects/docs/职场/文章标题_时间戳.md
```

## 高级功能

### 自定义模板
可以修改`templates/note-template.md`来自定义笔记格式。

### 浏览器集成
脚本可以与OpenClaw的浏览器工具集成，实现真正的网页内容提取。

### 批量处理
可以扩展脚本支持批量处理多个URL。

## 故障排除

### 常见问题
1. **Git操作失败**：检查git配置和网络连接
2. **内容提取失败**：URL可能受保护或需要登录
3. **保存路径不存在**：确保目录存在或有创建权限

### 调试模式
```bash
# 启用详细日志
DEBUG=true node scripts/save-notes.js <URL> <路径>
```

## 贡献
欢迎提交Issue和Pull Request来改进这个skill。

## 许可证
MIT License