#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
敏感词库合并脚本
Sensitive Words Merging Script

将 classified_vocabulary/ 目录下的所有分类敏感词库文件合并成一个完整的敏感词汇文件
"""

import os
import sys
from datetime import datetime, timezone
from typing import Dict, List, Tuple

class SensitiveWordsMerger:
    """敏感词库合并器"""
    
    def __init__(self):
        """初始化合并器"""
        self.classified_dir = "classified_vocabulary"
        self.output_file = "complete_sensitive_words.txt"
        
        # 分类信息：文件名、中文名称、处理级别、预期词汇数
        self.categories = [
            ("political.txt", "政治类词汇", "BLOCK", 2550),
            ("pornographic.txt", "色情类词汇", "BLOCK", 2819), 
            ("violent.txt", "暴力类词汇", "BLOCK", 1513),
            ("gambling.txt", "赌博类词汇", "BLOCK", 133),
            ("advertising.txt", "广告类词汇", "WARN", 19635),
            ("others.txt", "其他类词汇", "REVIEW", 16480)
        ]
        
        self.total_expected_words = 43130
    
    def read_vocabulary_file(self, filepath: str) -> List[str]:
        """读取单个词汇文件
        
        Args:
            filepath: 文件路径
            
        Returns:
            词汇列表
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                words = []
                for line in f:
                    word = line.strip()
                    if word and not word.startswith('#'):
                        words.append(word)
                return words
        except Exception as e:
            print(f"❌ 读取文件 {filepath} 失败: {e}")
            return []
    
    def load_all_categories(self) -> Dict[str, List[str]]:
        """加载所有分类词汇
        
        Returns:
            分类词汇字典
        """
        print("📚 开始加载分类词汇文件...")
        category_words = {}
        total_words = 0
        
        for filename, chinese_name, level, expected_count in self.categories:
            filepath = os.path.join(self.classified_dir, filename)
            
            if not os.path.exists(filepath):
                print(f"❌ 文件不存在: {filepath}")
                sys.exit(1)
            
            words = self.read_vocabulary_file(filepath)
            actual_count = len(words)
            
            print(f"✅ {chinese_name} ({filename}): {actual_count:,} 个词汇 (预期: {expected_count:,})")
            
            if actual_count != expected_count:
                print(f"⚠️ 警告: {filename} 词汇数量不匹配")
            
            category_words[filename] = words
            total_words += actual_count
        
        print(f"\n📊 总计加载: {total_words:,} 个词汇")
        
        if total_words != self.total_expected_words:
            print(f"⚠️ 警告: 总词汇数 {total_words:,} 不等于预期的 {self.total_expected_words:,}")
        
        return category_words
    
    def generate_file_header(self, total_words: int) -> str:
        """生成文件头部信息
        
        Args:
            total_words: 总词汇数
            
        Returns:
            头部信息字符串
        """
        current_time = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
        
        header = f"""# 完整敏感词汇库 - 基于 ComeOnMakeMoney/Sensitive-lexicon
# 版本：v1.0
# 词汇总数：{total_words:,} (去重后)
# 生成时间：{current_time}
# 数据来源：https://github.com/ComeOnMakeMoney/Sensitive-lexicon

"""
        return header
    
    def generate_category_section(self, filename: str, chinese_name: str, 
                                level: str, words: List[str]) -> str:
        """生成分类部分内容
        
        Args:
            filename: 文件名
            chinese_name: 中文名称
            level: 处理级别
            words: 词汇列表
            
        Returns:
            分类部分字符串
        """
        word_count = len(words)
        
        section = f"""# ============================================
# {chinese_name} [{level}] - {word_count:,} 个
# ============================================
"""
        
        # 添加所有词汇，每行一个
        for word in words:
            section += f"{word}\n"
        
        section += "\n"
        return section
    
    def merge_vocabularies(self) -> bool:
        """合并所有词汇文件
        
        Returns:
            合并是否成功
        """
        print("🚀 开始合并敏感词库...")
        
        # 加载所有分类词汇
        category_words = self.load_all_categories()
        
        if not category_words:
            print("❌ 没有加载到任何词汇")
            return False
        
        # 计算总词汇数
        total_words = sum(len(words) for words in category_words.values())
        
        # 生成合并文件
        print(f"📝 生成合并文件: {self.output_file}")
        
        try:
            with open(self.output_file, 'w', encoding='utf-8') as f:
                # 写入文件头部
                f.write(self.generate_file_header(total_words))
                
                # 按指定顺序写入各分类
                for filename, chinese_name, level, expected_count in self.categories:
                    if filename in category_words:
                        words = category_words[filename]
                        section = self.generate_category_section(
                            filename, chinese_name, level, words
                        )
                        f.write(section)
                        print(f"✅ 已写入 {chinese_name}: {len(words):,} 个词汇")
                    else:
                        print(f"⚠️ 跳过缺失的分类: {filename}")
        
        except Exception as e:
            print(f"❌ 生成文件失败: {e}")
            return False
        
        print(f"🎉 合并完成! 生成文件: {self.output_file}")
        print(f"📊 总词汇数: {total_words:,}")
        
        return True
    
    def generate_statistics(self) -> str:
        """生成统计信息
        
        Returns:
            统计信息字符串
        """
        category_words = self.load_all_categories()
        total_words = sum(len(words) for words in category_words.values())
        
        stats = f"""
合并统计信息:
=============
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
输出文件: {self.output_file}
总词汇数: {total_words:,}

分类统计:
"""
        
        for filename, chinese_name, level, expected_count in self.categories:
            if filename in category_words:
                actual_count = len(category_words[filename])
                percentage = (actual_count / total_words * 100) if total_words > 0 else 0
                stats += f"- {chinese_name}: {actual_count:,} 个 ({percentage:.1f}%)\n"
        
        return stats


def main():
    """主函数"""
    print("=" * 60)
    print("🔗 敏感词库合并工具")
    print("=" * 60)
    
    merger = SensitiveWordsMerger()
    
    # 检查输入目录
    if not os.path.exists(merger.classified_dir):
        print(f"❌ 分类词汇目录不存在: {merger.classified_dir}")
        return 1
    
    # 执行合并
    success = merger.merge_vocabularies()
    
    if success:
        # 显示统计信息
        stats = merger.generate_statistics()
        print(stats)
        
        # 验证输出文件
        if os.path.exists(merger.output_file):
            file_size = os.path.getsize(merger.output_file)
            print(f"✅ 输出文件大小: {file_size:,} 字节")
        
        print("🎯 合并任务完成!")
        return 0
    else:
        print("❌ 合并任务失败!")
        return 1


if __name__ == '__main__':
    sys.exit(main())