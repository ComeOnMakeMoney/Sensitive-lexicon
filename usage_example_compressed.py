#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
压缩JSON文件使用示例
Usage Example for Compressed JSON Files

演示如何在实际应用中使用压缩后的敏感词JSON文件
"""

import json
import gzip
import time
from typing import Set, List

class CompressedSensitiveWordLoader:
    """压缩敏感词文件加载器"""
    
    def __init__(self):
        """初始化加载器"""
        self.words = set()
        self.metadata = {}
    
    def load_original_format(self, filepath: str = "merged_sensitive_words.json"):
        """加载原始格式文件
        
        Args:
            filepath: 文件路径
        """
        print(f"📖 加载原始格式文件: {filepath}")
        start_time = time.time()
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.words = set(data['words'])
        self.metadata = {k: v for k, v in data.items() if k != 'words'}
        
        load_time = time.time() - start_time
        print(f"✅ 加载完成，耗时: {load_time:.3f}秒，词汇数量: {len(self.words):,}")
        return load_time
    
    def load_compressed_format(self, filepath: str = "merged_sensitive_words_compressed.json"):
        """加载JSON压缩格式文件
        
        Args:
            filepath: 文件路径
        """
        print(f"📖 加载JSON压缩格式文件: {filepath}")
        start_time = time.time()
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.words = set(data['words'])
        self.metadata = {k: v for k, v in data.items() if k != 'words'}
        
        load_time = time.time() - start_time
        print(f"✅ 加载完成，耗时: {load_time:.3f}秒，词汇数量: {len(self.words):,}")
        return load_time
    
    def load_gzip_format(self, filepath: str = "merged_sensitive_words_compressed.json.gz"):
        """加载GZIP压缩格式文件
        
        Args:
            filepath: 文件路径
        """
        print(f"📖 加载GZIP压缩格式文件: {filepath}")
        start_time = time.time()
        
        with gzip.open(filepath, 'rt', encoding='utf-8') as f:
            data = json.load(f)
        
        self.words = set(data['words'])
        self.metadata = {k: v for k, v in data.items() if k != 'words'}
        
        load_time = time.time() - start_time
        print(f"✅ 加载完成，耗时: {load_time:.3f}秒，词汇数量: {len(self.words):,}")
        return load_time
    
    def contains_sensitive_word(self, text: str) -> bool:
        """检查文本是否包含敏感词
        
        Args:
            text: 待检查的文本
            
        Returns:
            是否包含敏感词
        """
        text_lower = text.lower()
        return any(word.lower() in text_lower for word in self.words)
    
    def find_sensitive_words(self, text: str) -> List[str]:
        """查找文本中的所有敏感词
        
        Args:
            text: 待检查的文本
            
        Returns:
            找到的敏感词列表
        """
        text_lower = text.lower()
        found_words = []
        
        for word in self.words:
            if word.lower() in text_lower:
                found_words.append(word)
        
        return found_words
    
    def print_metadata(self):
        """打印元数据信息"""
        print("\n📋 敏感词库元数据:")
        for key, value in self.metadata.items():
            if key == 'categories':
                print(f"  📂 {key}: {list(value.keys())}")
            else:
                print(f"  📝 {key}: {value}")

def performance_comparison():
    """性能对比测试"""
    print("🚀 敏感词库加载性能对比测试")
    print("="*60)
    
    loader = CompressedSensitiveWordLoader()
    
    # 测试原始格式
    time1 = loader.load_original_format()
    
    # 测试JSON压缩格式
    time2 = loader.load_compressed_format()
    
    # 测试GZIP格式
    time3 = loader.load_gzip_format()
    
    # 显示元数据
    loader.print_metadata()
    
    print(f"\n📊 性能对比结果:")
    print(f"  原始格式:    {time1:.3f}秒")
    print(f"  JSON压缩:    {time2:.3f}秒 (相对原始: {time2/time1*100:.1f}%)")
    print(f"  GZIP压缩:    {time3:.3f}秒 (相对原始: {time3/time1*100:.1f}%)")
    
    return loader

def usage_example():
    """使用示例"""
    print("\n🧪 敏感词检测使用示例")
    print("="*60)
    
    # 加载压缩版本（推荐生产环境使用）
    loader = CompressedSensitiveWordLoader()
    loader.load_compressed_format()
    
    # 测试文本
    test_texts = [
        "这是一个正常的文本内容",
        "包含政治敏感词汇的内容",
        "这里有一些不当言论",
        "正常的技术讨论内容"
    ]
    
    print("🔍 敏感词检测结果:")
    for i, text in enumerate(test_texts, 1):
        print(f"\n  测试文本 {i}: {text}")
        
        # 检查是否包含敏感词
        has_sensitive = loader.contains_sensitive_word(text)
        print(f"  包含敏感词: {'❌ 是' if has_sensitive else '✅ 否'}")
        
        # 查找具体的敏感词
        if has_sensitive:
            found_words = loader.find_sensitive_words(text)
            print(f"  找到的敏感词: {found_words[:3]}{'...' if len(found_words) > 3 else ''}")

def main():
    """主函数"""
    print("🎯 压缩JSON文件使用示例演示")
    print("="*80)
    
    try:
        # 性能对比
        loader = performance_comparison()
        
        # 使用示例
        usage_example()
        
        print(f"\n💡 集成建议:")
        print(f"  1. 开发环境: 使用原始格式，便于调试")
        print(f"  2. 生产环境: 使用JSON压缩版本，减少内存占用")
        print(f"  3. 存储传输: 使用GZIP版本，最大化空间节省")
        print("="*80)
        
    except Exception as e:
        print(f"❌ 示例运行出错: {e}")

if __name__ == "__main__":
    main()