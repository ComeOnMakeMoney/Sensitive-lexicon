#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
敏感词分类结果验证脚本
Sensitive Word Classification Validation Script
"""

import os
import random
from classify_vocabulary import SensitiveWordClassifier

def test_classification():
    """测试分类结果的准确性"""
    classifier = SensitiveWordClassifier()
    
    # 测试样本
    test_cases = {
        'political': [
            '习近平', '胡锦涛', '江泽民', '法轮功', '轮功', '打倒共产党', 
            '台独', '藏独', '天安门', '六四', '共产主义', '民主党'
        ],
        'pornographic': [
            '色情', '淫乱', '做爱', '性交', '操逼', '爱液', '按摩棒',
            '裸体', '成人', 'A片', '黄片', '春宫'
        ],
        'violent': [
            '杀人', '暴力', '恐怖分子', '爆炸', '枪击', '血腥', '屠杀',
            '自杀', 'ISIS', '炸弹', '恐怖主义'
        ],
        'gambling': [
            '赌博', '老虎机', '百家乐', '轮盘', '六合彩', '时时彩',
            '赌场', '庄家', '下注', '押注'
        ],
        'advertising': [
            '办证', '代办', '快速办理', '低价', '促销', '贷款',
            '刷单', '兼职', '招聘', 'www.example.com', 'test.cn',
            '发票', '文凭'
        ]
    }
    
    print("🧪 测试分类准确性...")
    
    correct = 0
    total = 0
    
    for expected_category, words in test_cases.items():
        print(f"\n📋 测试类别: {expected_category}")
        for word in words:
            predicted = classifier.classify_word(word)
            total += 1
            if predicted == expected_category:
                correct += 1
                print(f"  ✅ {word} -> {predicted}")
            else:
                print(f"  ❌ {word} -> {predicted} (期望: {expected_category})")
    
    accuracy = correct / total * 100
    print(f"\n📊 分类准确率: {correct}/{total} = {accuracy:.1f}%")
    
    return accuracy > 70  # 要求70%以上准确率

def validate_output_files():
    """验证输出文件格式和内容"""
    output_dir = "classified_vocabulary"
    
    print("\n📁 验证输出文件...")
    
    if not os.path.exists(output_dir):
        print("❌ 输出目录不存在")
        return False
    
    # 检查必需文件
    required_files = [
        'political.txt', 'pornographic.txt', 'violent.txt',
        'gambling.txt', 'advertising.txt', 'others.txt',
        'README.md', 'statistics.txt'
    ]
    
    for filename in required_files:
        filepath = os.path.join(output_dir, filename)
        if os.path.exists(filepath):
            print(f"  ✅ {filename}")
        else:
            print(f"  ❌ {filename} 缺失")
            return False
    
    # 检查文件内容
    for filename in required_files:
        if filename.endswith('.txt') and filename != 'statistics.txt':
            filepath = os.path.join(output_dir, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    if len(lines) == 0:
                        print(f"  ⚠️  {filename} 为空")
                    else:
                        # 随机检查几行格式
                        sample_lines = random.sample(lines, min(3, len(lines)))
                        for line in sample_lines:
                            line = line.strip()
                            if len(line) == 0 or '\t' in line:
                                print(f"  ⚠️  {filename} 格式可能有问题: '{line}'")
            except Exception as e:
                print(f"  ❌ 读取 {filename} 失败: {e}")
                return False
    
    print("  ✅ 所有输出文件验证通过")
    return True

def check_deduplication():
    """检查去重效果"""
    print("\n🔍 检查去重效果...")
    
    output_dir = "classified_vocabulary"
    all_words = set()
    duplicates_found = False
    
    category_files = [
        'political.txt', 'pornographic.txt', 'violent.txt',
        'gambling.txt', 'advertising.txt', 'others.txt'
    ]
    
    for filename in category_files:
        filepath = os.path.join(output_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                words = [line.strip() for line in f.readlines() if line.strip()]
                category_words = set(words)
                
                # 检查类别内是否有重复
                if len(words) != len(category_words):
                    print(f"  ❌ {filename} 内部有重复词汇")
                    duplicates_found = True
                
                # 检查跨类别重复
                overlap = all_words.intersection(category_words)
                if overlap:
                    print(f"  ❌ {filename} 与其他类别有重复: {list(overlap)[:5]}...")
                    duplicates_found = True
                
                all_words.update(category_words)
    
    if not duplicates_found:
        print("  ✅ 未发现重复词汇")
    
    return not duplicates_found

def main():
    """主测试函数"""
    print("🚀 开始验证敏感词分类结果...\n")
    
    # 运行所有测试
    tests = [
        ("分类准确性测试", test_classification),
        ("输出文件验证", validate_output_files), 
        ("去重检查", check_deduplication)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"🧪 {test_name}")
        print('='*50)
        
        try:
            if test_func():
                print(f"✅ {test_name} 通过")
                passed += 1
            else:
                print(f"❌ {test_name} 失败")
        except Exception as e:
            print(f"❌ {test_name} 执行出错: {e}")
    
    print(f"\n{'='*50}")
    print(f"📊 验证结果: {passed}/{total} 测试通过")
    print('='*50)
    
    if passed == total:
        print("🎉 所有测试通过！分类结果良好。")
        return 0
    else:
        print("⚠️ 部分测试失败，请检查分类结果。")
        return 1

if __name__ == '__main__':
    exit(main())