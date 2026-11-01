#!/bin/bash

# Save Concept Events - Usage Examples

# Example 1: Single stock event
echo "=== Example 1: Single Stock Event ==="
node scripts/save-concept.js "金盘科技\n数据中心领域大幅增长" "科技行业" "AI概念"

echo ""
echo "=== Example 2: Multiple Stock Events ==="
node scripts/save-concept.js "金盘科技\n业绩基本符合预期，数据中心领域大幅增长\n\n拓普集团\n2025年业绩符合预期，机器人、液冷蓄势待发" "科技行业" "AI概念"

echo ""
echo "=== Example 3: Multiple Events, Different Industry ==="
node scripts/save-concept.js "比亚迪\n1月销量234.6万辆\n\n宁德时代\n1月动力电池装车量稳步增长" "汽车行业" "新能源汽车"

echo ""
echo "=== Example 4: Multiple Events, Different Concept ==="
node scripts/save-concept.js "贵州茅台\n春节消费潜力释放，业绩基本符合预期\n\n五粮液\n白酒行业景气度高，业绩稳步增长" "消费行业" "白酒"

echo ""
echo "=== Example 5: Complex Text from Email Summary ==="
node scripts/save-concept.js "金盘科技\n业绩基本符合预期，数据中心领域大幅增长\n\n拓普集团\n2025年业绩符合预期，机器人、液冷蓄势待发\n\n隆基绿能\n融资买入3.50亿元，融资余额62.88亿元" "科技行业" "光伏概念"

echo ""
echo "=== Example 6: Save Concept Stocks Only ==="
node scripts/save-concept.js stocks "AI应用" "寒武纪,中科曙光,海光信息"

echo ""
echo "=== Example 7: Save Concept Stocks From Newline List ==="
node scripts/save-concept.js stocks "液冷服务器" "英维克
高澜股份
申菱环境"

echo ""
echo "All examples completed!"
