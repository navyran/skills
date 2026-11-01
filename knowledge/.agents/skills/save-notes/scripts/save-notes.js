#!/usr/bin/env node

/**
 * 保存笔记工具 v2.0
 * 使用 agent-browser 从网页提取内容，生成结构化笔记，并自动 git 提交
 * 
 * 用法: node scripts/save-notes.js <文章URL> <笔记标题> [标签列表（逗号分隔）]
 * 示例: node scripts/save-notes.js "https://example.com/article" "文章标题" "AI,编程"
 */

const fs = require('fs');
const path = require('path');
const { execSync, spawnSync } = require('child_process');

// 配置
const CONFIG = {
  savePath: path.join(process.env.HOME, 'PycharmProjects', 'docs'),
  gitAutoCommit: true
};

// 获取 Git 仓库根目录（保存路径）
function getRepoRoot() {
  return CONFIG.savePath;
}

/**
 * 主函数
 */
async function main() {
  const args = process.argv.slice(2);
  
  if (args.length < 2) {
    console.error('❌ 参数错误');
    console.error('用法: node scripts/save-notes.js <文章URL> <笔记标题> [标签列表]');
    console.error('示例: node scripts/save-notes.js "https://example.com/article" "文章标题" "AI,编程"');
    process.exit(1);
  }

  const [url, title, tagsArg = ''] = args;
  const tags = tagsArg.split(',').map(t => t.trim()).filter(Boolean);
  
  console.log('📝 开始保存笔记...');
  console.log(`   URL: ${url}`);
  console.log(`   标题: ${title}`);
  console.log(`   标签: ${tags.join(', ') || '无'}`);
  
  try {
    // 1. 使用 agent-browser 提取文章内容
    console.log('\n🔍 正在使用浏览器提取文章内容...');
    const articleContent = await extractArticleContent(url);
    
    // 2. 生成结构化笔记
    console.log('📄 正在生成结构化笔记...');
    const noteContent = generateNote(title, url, articleContent, tags);
    
    // 3. 保存文件
    console.log('💾 正在保存文件...');
    const filePath = saveNoteFile(title, noteContent);
    
    // 4. Git 提交
    if (CONFIG.gitAutoCommit) {
      console.log('🔄 正在执行 Git 提交...');
      gitCommit(filePath, title);
    }
    
    console.log('\n✅ 笔记保存完成！');
    console.log(`   📄 文件: ${filePath}`);
    
  } catch (error) {
    console.error('\n❌ 保存笔记失败:', error.message);
    console.error(error.stack);
    process.exit(1);
  } finally {
    // 确保关闭浏览器
    try {
      execSync('agent-browser close 2>/dev/null || true', { stdio: 'ignore' });
    } catch (e) {}
  }
}

/**
 * 使用 agent-browser 提取文章内容
 */
async function extractArticleContent(url) {
  return new Promise((resolve, reject) => {
    // 打开网页
    const openResult = spawnSync('agent-browser', ['open', url], {
      encoding: 'utf8',
      timeout: 15000
    });
    
    if (openResult.status !== 0 && !openResult.stdout.includes('✓')) {
      console.log('   ⚠️  浏览器打开可能遇到问题，继续尝试...');
    }
    
    // 等待页面加载
    spawnSync('agent-browser', ['wait', '3000'], { encoding: 'utf8', timeout: 5000 });
    
    // 获取页面快照（获取主要内容区域）
    const snapshotResult = spawnSync('agent-browser', ['snapshot', '-c', '-d', '5'], {
      encoding: 'utf8',
      timeout: 15000
    });
    
    if (snapshotResult.error) {
      throw new Error(`获取页面快照失败: ${snapshotResult.error.message}`);
    }
    
    // 尝试点击"展开"按钮（如果有）
    if (snapshotResult.stdout.includes('展开剩余') || snapshotResult.stdout.includes('点击展开')) {
      console.log('   📌 检测到折叠内容，尝试展开...');
      spawnSync('agent-browser', ['click', '--text', '展开'], { encoding: 'utf8', timeout: 5000 });
      spawnSync('agent-browser', ['wait', '2000'], { encoding: 'utf8', timeout: 5000 });
      
      // 重新获取快照
      const retryResult = spawnSync('agent-browser', ['snapshot', '-c', '-d', '5'], {
        encoding: 'utf8',
        timeout: 15000
      });
      if (retryResult.stdout) {
        resolve(retryResult.stdout);
        return;
      }
    }
    
    // 返回快照内容
    resolve(snapshotResult.stdout || '无法提取页面内容');
  });
}

/**
 * 生成结构化笔记内容
 */
function generateNote(title, url, rawContent, tags = []) {
  const now = new Date();
  const dateStr = now.toLocaleDateString('zh-CN');
  const timeStr = now.toLocaleTimeString('zh-CN');
  
  // 处理内容，移除多余的导航、广告等
  let content = rawContent
    .replace(/banner:[\s\S]*?main:/g, '')  // 移除顶部 banner
    .replace(/complementary[\s\S]*$/g, '') // 移除侧边栏
    .replace(/region "评论区"[\s\S]*$/g, '') // 移除评论区
    .replace(/region "相关推荐"[\s\S]*$/g, '') // 移除推荐
    .trim();
  
  // 如果内容太短，直接使用原始内容
  if (content.length < 100) {
    content = rawContent;
  }

  return `# ${title}

## 基本信息
- **来源**: ${url}
- **保存时间**: ${dateStr} ${timeStr}
- **标签**: ${tags.length ? tags.map(t => `#${t}`).join(' ') : '#笔记'}

## 文章内容

\`\`\`raw
${content}
\`\`\`

## 备注

---

*由 OpenClaw save-notes skill 自动生成*
*v2.0.0*
`;
}

/**
 * 保存笔记文件
 */
function saveNoteFile(title, content) {
  // 确保保存路径存在
  if (!fs.existsSync(CONFIG.savePath)) {
    fs.mkdirSync(CONFIG.savePath, { recursive: true });
  }
  
  // 生成安全的文件名
  const safeFileName = title
    .replace(/[<>:"/\\|?*]/g, '')
    .replace(/\s+/g, '-')
    .replace(/[，。！？、；：""''（）【】]/g, '-')
    .replace(/-+/g, '-')
    .replace(/^-|-$/g, '')
    .substring(0, 80)
    .toLowerCase();
  
  const fileName = `${safeFileName}.md`;
  const filePath = path.join(CONFIG.savePath, fileName);
  
  // 如果文件已存在，添加时间戳
  if (fs.existsSync(filePath)) {
    const timestamp = Date.now();
    const filePathAlt = path.join(CONFIG.savePath, `${safeFileName}_${timestamp}.md`);
    fs.writeFileSync(filePathAlt, content, 'utf8');
    return filePathAlt;
  }
  
  fs.writeFileSync(filePath, content, 'utf8');
  return filePath;
}

/**
 * Git 提交
 */
function gitCommit(filePath, title) {
  try {
    const repoRoot = getRepoRoot();
    
    // 切换到仓库目录
    process.chdir(repoRoot);
    
    // 添加文件
    const relativePath = path.relative(repoRoot, filePath);
    execSync(`git add "${relativePath}"`, { stdio: 'ignore' });
    
    // 提交
    const commitMessage = `添加笔记: ${title.substring(0, 60)}`;
    execSync(`git commit -m "${commitMessage}"`, { stdio: 'ignore' });
    
    console.log('   ✅ Git 提交成功');
    
  } catch (error) {
    console.log('   ⚠️  Git 操作遇到问题，可能已提交或需要手动处理');
  }
}

// 运行主函数
if (require.main === module) {
  main().catch(console.error);
}

module.exports = {
  extractArticleContent,
  generateNote,
  saveNoteFile,
  gitCommit
};
