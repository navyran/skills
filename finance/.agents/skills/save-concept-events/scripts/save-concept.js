#!/usr/bin/env node

/**
 * Save Concept Events Script
 * Calls module_func APIs to save stock concept events or concept stock lists.
 * Automatically generates a K-line chart link after successful save.
 */

const https = require('https');

const API_OPTIONS = {
  hostname: 'pi.navyran.top',
  port: 3001,
  path: '/devops/module_func',
  method: 'POST'
};

/**
 * Extract stock names from the input text
 * @param {string} txt - Stock event text in format "股票名称\n事件描述\n\n股票名称 2\n事件描述 2"
 * @returns {string[]} Array of stock names
 */
function extractStockNames(txt) {
  const lines = txt.split('\n').filter(line => line.trim());
  const stockNames = [];
  
  // Stock names appear on odd positions (0, 2, 4, ...) when format is "name\ndesc\n\nname\ndesc"
  for (let i = 0; i < lines.length; i += 2) {
    const name = lines[i].trim();
    if (name) {
      stockNames.push(name);
    }
  }
  
  return stockNames;
}

/**
 * Generate K-line chart URL with URL-encoded parameters
 * @param {string[]} stockNames - Array of stock names
 * @returns {string} URL-encoded link
 */
function generateKLineLink(stockNames) {
  const baseUrl = 'https://pi.navyran.top:8501/';
  const page = encodeURIComponent('K' + '线筹码');
  const namestr = encodeURIComponent(stockNames.join(','));
  
  return `${baseUrl}?page=${page}&namestr=${namestr}`;
}

/**
 * Normalize a stock list string to unique stock names.
 * @param {string|string[]} stockList - Comma, Chinese comma, whitespace, or newline separated stock names
 * @returns {string[]} Unique stock names
 */
function normalizeStockNames(stockList) {
  const source = Array.isArray(stockList) ? stockList.join(',') : String(stockList || '');
  const stockNames = source
    .split(/[,，\n\r\t ]+/)
    .map(name => name.trim())
    .filter(Boolean);

  return Array.from(new Set(stockNames));
}

/**
 * Call the FastAPI module_func endpoint.
 * @param {string} funcName - mystock function name
 * @param {object} funcKwargsJson - Function kwargs
 * @returns {Promise<object>} API response
 */
function postMystockModuleFunc(funcName, funcKwargsJson) {
  const payload = {
    module: 'mystock',
    func_name: funcName,
    func_kwargs_json: funcKwargsJson
  };

  return new Promise((resolve, reject) => {
    const postData = JSON.stringify(payload);

    const options = {
      ...API_OPTIONS,
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(postData)
      }
    };

    const req = https.request(options, (res) => {
      let data = '';

      res.on('data', (chunk) => {
        data += chunk;
      });

      res.on('end', () => {
        try {
          const response = JSON.parse(data);
          if (res.statusCode === 200) {
            console.log('✅ Success:', JSON.stringify(response, null, 2));
            resolve(response);
          } else {
            console.error('❌ Error:', res.statusCode, response);
            reject(new Error(`HTTP ${res.statusCode}: ${JSON.stringify(response)}`));
          }
        } catch (e) {
          console.error('❌ Parse Error:', e.message);
          console.error('Raw response:', data);
          reject(e);
        }
      });
    });

    req.on('error', (e) => {
      console.error('❌ Request Error:', e.message);
      reject(e);
    });

    req.write(postData);
    req.end();
  });
}

/**
 * Main function to save concept events
 * @param {string} txt - Stock event text in format "股票名称\n事件描述\n\n股票名称 2\n事件描述 2"
 * @param {string} industry_in - Industry classification
 * @param {string} concept_in - Concept category
 */
async function saveConceptEvents(txt, industry_in, concept_in) {
  return postMystockModuleFunc('parse_txt_and_save_event_and_save_concept', {
    txt: txt,
    industry_in: industry_in,
    concept_in: concept_in
  });
}

/**
 * Save concept stocks only.
 * @param {string} concept - Concept name
 * @param {string|string[]} stockList - Stock names
 */
async function saveConceptStocks(concept, stockList) {
  const conceptName = String(concept || '').trim();
  const stockNames = normalizeStockNames(stockList);

  if (!conceptName) {
    throw new Error('concept is required');
  }
  if (stockNames.length === 0) {
    throw new Error('stock list is required');
  }

  return postMystockModuleFunc('save_stock_to_concept_db', {
    concept: conceptName,
    namestr: stockNames.join(',')
  });
}

function printUsage() {
  console.log('Usage:');
  console.log('  node save-concept.js <txt> <industry_in> <concept_in>');
  console.log('  node save-concept.js events <txt> <industry_in> <concept_in>');
  console.log('  node save-concept.js stocks <concept> <stock_names>');
  console.log('');
  console.log('Parameters:');
  console.log('  txt          - Stock event text in format "股票名称\\n事件描述\\n\\n股票名称 2\\n事件描述 2"');
  console.log('  industry_in  - Industry classification');
  console.log('  concept_in   - Concept category');
  console.log('  concept      - Concept name saved to the stock concept library');
  console.log('  stock_names  - Stock names separated by comma, Chinese comma, space, or newline');
  console.log('');
  console.log('Examples:');
  console.log('  node save-concept.js "金盘科技\\n数据中心领域大幅增长" "科技行业" "AI 概念"');
  console.log('  node save-concept.js stocks "AI应用" "寒武纪,中科曙光,海光信息"');
}

/**
 * Parse command line arguments
 */
function parseArgs() {
  const args = process.argv.slice(2);

  if (args[0] === 'events') {
    if (args.length < 4) {
      printUsage();
      process.exit(1);
    }
    return {
      mode: 'events',
      txt: args[1],
      industry_in: args[2],
      concept_in: args[3]
    };
  }

  if (args[0] === 'stocks') {
    if (args.length < 3) {
      printUsage();
      process.exit(1);
    }
    return {
      mode: 'stocks',
      concept: args[1],
      stockList: args.slice(2).join(',')
    };
  }

  if (args.length < 3) {
    printUsage();
    process.exit(1);
  }

  return {
    mode: 'events',
    txt: args[0],
    industry_in: args[1],
    concept_in: args[2]
  };
}

/**
 * Main entry point
 */
async function main() {
  try {
    const args = parseArgs();

    if (args.mode === 'stocks') {
      const stockNames = normalizeStockNames(args.stockList);

      console.log('📋 Saving Concept Stocks...');
      console.log('----------------------------------------');
      console.log('Concept:', args.concept);
      console.log('Stocks:', stockNames.join(','));
      console.log('----------------------------------------');

      await saveConceptStocks(args.concept, args.stockList);

      const kLineLink = generateKLineLink(stockNames);

      console.log('');
      console.log('✅ Concept stocks saved successfully!');
      console.log('');
      console.log(`📊 股票数量：${stockNames.length}只`);
      console.log(`📈 K 线筹码链接：${kLineLink}`);

      process.exit(0);
    }

    const { txt, industry_in, concept_in } = args;

    console.log('📋 Saving Concept Events...');
    console.log('----------------------------------------');
    console.log('Text:', txt);
    console.log('Industry:', industry_in);
    console.log('Concept:', concept_in);
    console.log('----------------------------------------');

    const result = await saveConceptEvents(txt, industry_in, concept_in);

    // Extract stock names and generate K-line link
    const stockNames = extractStockNames(txt);
    const kLineLink = generateKLineLink(stockNames);

    console.log('');
    console.log('✅ Concept events saved successfully!');
    console.log('');
    console.log(`📊 股票数量：${stockNames.length}只`);
    console.log(`📈 K 线筹码链接：${kLineLink}`);
    
    process.exit(0);
  } catch (error) {
    console.error('');
    console.error('❌ Failed to save concept events:', error.message);
    process.exit(1);
  }
}

// Run if executed directly
if (require.main === module) {
  main();
}

module.exports = {
  saveConceptEvents,
  saveConceptStocks,
  extractStockNames,
  normalizeStockNames,
  generateKLineLink
};
