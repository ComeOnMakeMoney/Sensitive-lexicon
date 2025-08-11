#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试敏感词库合并和JSON转换脚本
Test script for sensitive lexicon merging and JSON conversion
"""

import os
import json
import tempfile
import shutil
from merge_to_json import SensitiveWordMerger


def test_merge_to_json():
    """测试合并和JSON转换功能"""
    print("🧪 开始测试敏感词库合并和JSON转换...")
    
    # 创建临时测试环境
    with tempfile.TemporaryDirectory() as temp_dir:
        # 创建测试用的词汇目录
        test_vocab_dir = os.path.join(temp_dir, "Vocabulary")
        os.makedirs(test_vocab_dir)
        
        # 创建测试词汇文件
        test_files = {
            "政治词库.txt": ["习近平", "共产党", "# 这是注释", "", "民主"],
            "色情词库.txt": ["色情", "成人", "# 注释行", "裸体"],
            "其他词库.txt": ["测试词汇", "示例", "习近平"]  # 包含重复词汇
        }
        
        for filename, words in test_files.items():
            filepath = os.path.join(test_vocab_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write('\n'.join(words))
        
        # 保存当前目录
        original_dir = os.getcwd()
        
        try:
            # 切换到临时目录
            os.chdir(temp_dir)
            
            # 运行合并器
            merger = SensitiveWordMerger()
            success = merger.run()
            
            if not success:
                print("❌ 合并和转换失败")
                return False
            
            # 验证生成的文件
            if not os.path.exists(merger.merged_file):
                print(f"❌ 合并文件 {merger.merged_file} 未生成")
                return False
            
            if not os.path.exists(merger.json_file):
                print(f"❌ JSON文件 {merger.json_file} 未生成")
                return False
            
            # 验证合并文件内容
            with open(merger.merged_file, 'r', encoding='utf-8') as f:
                merged_content = f.read()
            
            # 检查是否包含预期的词汇
            expected_words = ["习近平", "共产党", "民主", "色情", "成人", "裸体", "测试词汇", "示例"]
            for word in expected_words:
                if word not in merged_content:
                    print(f"❌ 合并文件缺少词汇: {word}")
                    return False
            
            # 检查是否过滤了注释
            if "# 这是注释" in merged_content or "# 注释行" in merged_content:
                print("❌ 合并文件包含注释行")
                return False
            
            # 验证JSON文件
            with open(merger.json_file, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
            
            # 验证JSON结构
            required_keys = ['metadata', 'words']
            for key in required_keys:
                if key not in json_data:
                    print(f"❌ JSON文件缺少字段: {key}")
                    return False
            
            # 验证metadata字段
            metadata = json_data['metadata']
            required_metadata = ['source_file', 'converted_time', 'total_words', 'description']
            for key in required_metadata:
                if key not in metadata:
                    print(f"❌ JSON metadata缺少字段: {key}")
                    return False
            
            # 验证词汇数量
            words_list = json_data['words']
            if metadata['total_words'] != len(words_list):
                print(f"❌ 词汇数量不匹配: metadata={metadata['total_words']}, actual={len(words_list)}")
                return False
            
            # 验证去重效果 (习近平应该只出现一次)
            word_count = words_list.count("习近平")
            if word_count != 1:
                print(f"❌ 去重失败，'习近平'出现了 {word_count} 次")
                return False
            
            # 验证所有预期词汇都在JSON中
            for word in expected_words:
                if word not in words_list:
                    print(f"❌ JSON文件缺少词汇: {word}")
                    return False
            
            print(f"✅ 测试通过！")
            print(f"📊 合并了 {len(words_list)} 个不重复的词汇")
            print(f"📝 元数据: {metadata}")
            
            return True
            
        finally:
            # 恢复原目录
            os.chdir(original_dir)


def test_existing_files():
    """测试现有的合并和JSON文件"""
    print("\n🧪 测试现有的合并和JSON文件...")
    
    # 检查文件是否存在
    files_to_check = ["merged_sensitive_words.txt", "merged_sensitive_words.json"]
    for file in files_to_check:
        if not os.path.exists(file):
            print(f"❌ 文件不存在: {file}")
            return False
    
    # 验证JSON文件
    try:
        with open("merged_sensitive_words.json", 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        
        # 基本结构检查
        if 'metadata' not in json_data or 'words' not in json_data:
            print("❌ JSON文件结构不正确")
            return False
        
        # 检查词汇数量
        metadata = json_data['metadata']
        words_list = json_data['words']
        
        if metadata['total_words'] != len(words_list):
            print(f"❌ 词汇数量不匹配")
            return False
        
        print(f"✅ 现有文件验证通过！")
        print(f"📊 包含 {len(words_list)} 个词汇")
        print(f"🕒 转换时间: {metadata['converted_time']}")
        
        return True
        
    except Exception as e:
        print(f"❌ JSON文件验证失败: {e}")
        return False


def main():
    """主测试函数"""
    print("🚀 开始测试敏感词库合并和JSON转换功能\n")
    
    # 测试1: 基本功能测试
    test1_passed = test_merge_to_json()
    
    # 测试2: 现有文件测试
    test2_passed = test_existing_files()
    
    # 总结
    print(f"\n{'='*50}")
    print(f"📊 测试结果汇总")
    print(f"{'='*50}")
    
    tests = [
        ("基本功能测试", test1_passed),
        ("现有文件验证", test2_passed)
    ]
    
    passed = sum(1 for _, result in tests if result)
    total = len(tests)
    
    for test_name, result in tests:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name}: {status}")
    
    print(f"\n📈 总体结果: {passed}/{total} 测试通过")
    
    if passed == total:
        print("🎉 所有测试都通过了！")
        return 0
    else:
        print("⚠️  部分测试失败，请检查问题")
        return 1


if __name__ == '__main__':
    exit(main())