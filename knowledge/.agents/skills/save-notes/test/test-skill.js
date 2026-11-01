#!/usr/bin/env node

/**
 * 测试保存笔记Skill
 */

const path = require('path');
const fs = require('fs');

// 导入skill模块
const saveNotes = require('../scripts/save-notes.js');

// 测试配置
const TEST_CONFIG = {
  testUrl: 'https://example.com/test-article',
  testSavePath: path.join(__dirname, 'test-output'),
  testCategory: '测试分类'
};

// 清理测试目录
function cleanupTestDir() {
  const testDir = TEST_CONFIG.testSavePath;
  if (fs.existsSync(testDir)) {
    fs.rmSync(testDir, { recursive: true, force: true });
  }
  fs.mkdirSync(testDir, { recursive: true });
}

// 测试内容提取
async function testExtractContent() {
  console.log('🧪 测试内容提取...');
  
  try {
    const content = await saveNotes.extractArticleContent(TEST_CONFIG.testUrl);
    
    console.log('✅ 内容提取测试通过');
    console.log(`   标题: ${content.title}`);
    console.log(`   作者: ${content.author}`);
    console.log(`   日期: ${content.date}`);
    
    return content;
  } catch (error) {
    console.log('❌ 内容提取测试失败:', error.message);
    return null;
  }
}

// 测试笔记生成
function testNoteGeneration(articleContent) {
  console.log('🧪 测试笔记生成...');
  
  try {
    const note = saveNotes.generateNote(
      articleContent,
      TEST_CONFIG.testUrl,
      TEST_CONFIG.testCategory
    );
    
    console.log('✅ 笔记生成测试通过');
    console.log(`   笔记长度: ${note.length} 字符`);
    
    // 检查必要部分
    const checks = [
      { name: '标题', check: note.includes(articleContent.title) },
      { name: 'URL', check: note.includes(TEST_CONFIG.testUrl) },
      { name: '分类', check: note.includes(TEST_CONFIG.testCategory) },
      { name: '时间戳', check: note.includes('自动生成于') }
    ];
    
    checks.forEach(check => {
      console.log(`   ${check.check ? '✅' : '❌'} ${check.name}`);
    });
    
    return note;
  } catch (error) {
    console.log('❌ 笔记生成测试失败:', error.message);
    return null;
  }
}

// 测试文件保存
function testFileSave(noteContent) {
  console.log('🧪 测试文件保存...');
  
  try {
    const filePath = saveNotes.saveNoteFile(
      noteContent,
      TEST_CONFIG.testSavePath,
      '测试文章标题'
    );
    
    console.log('✅ 文件保存测试通过');
    console.log(`   文件路径: ${filePath}`);
    console.log(`   文件存在: ${fs.existsSync(filePath)}`);
    
    const stats = fs.statSync(filePath);
    console.log(`   文件大小: ${stats.size} 字节`);
    
    return filePath;
  } catch (error) {
    console.log('❌ 文件保存测试失败:', error.message);
    return null;
  }
}

// 测试Git检查
function testGitCheck() {
  console.log('🧪 测试Git仓库检查...');
  
  try {
    const isGitRepo = saveNotes.isGitRepository(TEST_CONFIG.testSavePath);
    
    console.log(`✅ Git检查测试通过`);
    console.log(`   是否是Git仓库: ${isGitRepo ? '是' : '否'}`);
    
    return isGitRepo;
  } catch (error) {
    console.log('❌ Git检查测试失败:', error.message);
    return false;
  }
}

// 主测试函数
async function runTests() {
  console.log('🚀 开始保存笔记Skill测试\n');
  
  // 清理并准备测试目录
  cleanupTestDir();
  
  // 运行测试
  const testResults = {
    extractContent: false,
    noteGeneration: false,
    fileSave: false,
    gitCheck: false
  };
  
  // 测试1：内容提取
  const articleContent = await testExtractContent();
  testResults.extractContent = !!articleContent;
  
  if (articleContent) {
    // 测试2：笔记生成
    const noteContent = testNoteGeneration(articleContent);
    testResults.noteGeneration = !!noteContent;
    
    if (noteContent) {
      // 测试3：文件保存
      const filePath = testFileSave(noteContent);
      testResults.fileSave = !!filePath;
    }
  }
  
  // 测试4：Git检查
  testResults.gitCheck = testGitCheck();
  
  // 输出测试总结
  console.log('\n📊 测试总结');
  console.log('=' .repeat(40));
  
  Object.entries(testResults).forEach(([testName, passed]) => {
    console.log(`${passed ? '✅' : '❌'} ${testName}: ${passed ? '通过' : '失败'}`);
  });
  
  const totalTests = Object.keys(testResults).length;
  const passedTests = Object.values(testResults).filter(Boolean).length;
  const score = Math.round((passedTests / totalTests) * 100);
  
  console.log('\n🎯 测试结果');
  console.log(`   通过: ${passedTests}/${totalTests}`);
  console.log(`   得分: ${score}%`);
  
  if (score >= 75) {
    console.log('🌟 Skill基本功能测试通过！');
  } else {
    console.log('⚠️  Skill需要进一步调试');
  }
  
  // 清理测试文件
  cleanupTestDir();
  
  return score >= 75;
}

// 运行测试
if (require.main === module) {
  runTests().then(success => {
    process.exit(success ? 0 : 1);
  }).catch(error => {
    console.error('测试运行失败:', error);
    process.exit(1);
  });
}

module.exports = {
  runTests,
  TEST_CONFIG
};