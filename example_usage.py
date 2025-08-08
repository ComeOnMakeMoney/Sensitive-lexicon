#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
敏感词检测示例
Sensitive Word Detection Example

展示如何使用分类后的敏感词库进行文本过滤
"""

import os
import re
from typing import Dict, List, Set

class SensitiveWordDetector:
    """敏感词检测器"""
    
    def __init__(self, vocabulary_dir: str = "classified_vocabulary"):
        """初始化检测器
        
        Args:
            vocabulary_dir: 分类词库目录
        """
        self.vocabulary_dir = vocabulary_dir
        self.word_sets = {}
        self.load_vocabularies()
    
    def load_vocabularies(self):
        """加载分类词库"""
        categories = ['political', 'pornographic', 'violent', 'gambling', 'advertising', 'others']
        
        for category in categories:
            filename = f"{category}.txt"
            filepath = os.path.join(self.vocabulary_dir, filename)
            
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    words = {line.strip() for line in f if line.strip()}
                    self.word_sets[category] = words
                    print(f"✅ 加载 {category}: {len(words)} 个词汇")
            else:
                self.word_sets[category] = set()
                print(f"⚠️ 文件不存在: {filepath}")
    
    def detect_sensitive_words(self, text: str) -> Dict[str, List[str]]:
        """检测文本中的敏感词
        
        Args:
            text: 待检测的文本
            
        Returns:
            字典，键为类别，值为检测到的敏感词列表
        """
        results = {}
        
        for category, words in self.word_sets.items():
            found_words = []
            for word in words:
                if word in text:
                    found_words.append(word)
            
            if found_words:
                results[category] = found_words
        
        return results
    
    def filter_text(self, text: str, replacement: str = "*") -> str:
        """过滤文本中的敏感词
        
        Args:
            text: 原始文本
            replacement: 替换字符
            
        Returns:
            过滤后的文本
        """
        filtered_text = text
        
        for category, words in self.word_sets.items():
            for word in words:
                if word in filtered_text:
                    filtered_text = filtered_text.replace(word, replacement * len(word))
        
        return filtered_text
    
    def get_statistics(self) -> Dict[str, int]:
        """获取词库统计信息"""
        return {category: len(words) for category, words in self.word_sets.items()}


def main():
    """示例主函数"""
    print("🚀 敏感词检测示例")
    print("=" * 50)
    
    # 初始化检测器
    detector = SensitiveWordDetector()
    
    # 显示统计信息
    stats = detector.get_statistics()
    print(f"\n📊 词库统计:")
    for category, count in stats.items():
        print(f"  {category}: {count:,} 个词汇")
    
    # 测试文本
    test_texts = [
        "这是一个正常的文本，没有敏感词。",
        "这个网站提供快速办证服务，请联系QQ123456。",
        "政治敏感内容测试。",
        "这里包含一些不当内容。",
    ]
    
    print(f"\n🧪 检测示例:")
    print("-" * 50)
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n测试文本 {i}: {text}")
        
        # 检测敏感词
        detected = detector.detect_sensitive_words(text)
        
        if detected:
            print("  检测到敏感词:")
            for category, words in detected.items():
                print(f"    {category}: {words}")
        else:
            print("  ✅ 未检测到敏感词")
        
        # 过滤文本
        filtered = detector.filter_text(text)
        if filtered != text:
            print(f"  过滤后: {filtered}")


if __name__ == '__main__':
    main()