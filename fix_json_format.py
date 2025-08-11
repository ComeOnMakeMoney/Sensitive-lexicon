#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
敏感词库JSON格式修复脚本
Sensitive Words JSON Format Fix Script

该脚本用于修复 merged_sensitive_words.json 文件中的格式问题，
主要解决逗号分隔词汇被错误地合并为单个条目的问题。

修复内容：
1. 重新读取原始的敏感词汇文件
2. 正确解析每一行，确保每个词汇都是独立的JSON数组元素
3. 处理包含逗号分隔的词汇行
4. 重新生成正确格式的JSON文件
"""

import os
import json
import logging
from datetime import datetime
from typing import List, Set, Dict, Any

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('fix_json_format.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class SensitiveWordsJSONFixer:
    """敏感词库JSON格式修复器"""
    
    def __init__(self):
        """初始化修复器"""
        self.vocabulary_dir = "Vocabulary"
        self.output_txt = "merged_sensitive_words.txt"
        self.output_json = "merged_sensitive_words.json"
        self.words_set = set()  # 使用集合去重
        
    def read_vocabulary_files(self) -> Set[str]:
        """
        读取所有词汇文件
        
        Returns:
            Set[str]: 去重后的敏感词集合
        """
        words = set()
        
        if not os.path.exists(self.vocabulary_dir):
            logger.error(f"词汇目录不存在: {self.vocabulary_dir}")
            return words
            
        # 遍历词汇目录中的所有txt文件
        for filename in os.listdir(self.vocabulary_dir):
            if not filename.endswith('.txt'):
                continue
                
            file_path = os.path.join(self.vocabulary_dir, filename)
            logger.info(f"正在处理文件: {filename}")
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line_num, line in enumerate(f, 1):
                        line = line.strip()
                        
                        # 跳过空行和注释行
                        if not line or line.startswith('#'):
                            continue
                            
                        # 处理逗号分隔的词汇
                        if ',' in line:
                            # 按逗号分割并处理每个词汇
                            for word in line.split(','):
                                word = word.strip()
                                if word:  # 确保不是空字符串
                                    words.add(word)
                                    
                        else:
                            # 单个词汇
                            words.add(line)
                            
            except Exception as e:
                logger.error(f"读取文件 {filename} 时出错: {e}")
                continue
                
        logger.info(f"总共读取到 {len(words)} 个唯一敏感词")
        return words
        
    def create_merged_txt(self, words: Set[str]) -> bool:
        """
        创建合并的txt文件
        
        Args:
            words: 敏感词集合
            
        Returns:
            bool: 是否成功创建
        """
        try:
            # 排序词汇以便于查看和比较
            sorted_words = sorted(words)
            
            with open(self.output_txt, 'w', encoding='utf-8') as f:
                f.write("# 合并敏感词库\n")
                f.write(f"# 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"# 词汇总数: {len(sorted_words)}\n")
                f.write("\n")
                
                for word in sorted_words:
                    f.write(f"{word}\n")
                    
            logger.info(f"成功创建合并的txt文件: {self.output_txt}")
            return True
            
        except Exception as e:
            logger.error(f"创建txt文件时出错: {e}")
            return False
            
    def create_merged_json(self, words: Set[str]) -> bool:
        """
        创建合并的JSON文件
        
        Args:
            words: 敏感词集合
            
        Returns:
            bool: 是否成功创建
        """
        try:
            # 排序词汇以便于查看和比较
            sorted_words = sorted(words)
            
            # 创建JSON结构
            json_data = {
                "lastUpdateDate": datetime.now().strftime('%Y/%m/%d'),
                "totalCount": len(sorted_words),
                "description": "中文敏感词库 - 已修复格式问题",
                "words": sorted_words
            }
            
            # 写入JSON文件，确保UTF-8编码和中文字符正确显示
            with open(self.output_json, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=2)
                
            logger.info(f"成功创建合并的JSON文件: {self.output_json}")
            return True
            
        except Exception as e:
            logger.error(f"创建JSON文件时出错: {e}")
            return False
            
    def generate_statistics(self, words: Set[str]) -> Dict[str, Any]:
        """
        生成统计信息
        
        Args:
            words: 敏感词集合
            
        Returns:
            Dict[str, Any]: 统计信息
        """
        stats = {
            "total_words": len(words),
            "generation_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "source_files": [],
            "word_length_distribution": {}
        }
        
        # 统计词汇长度分布
        length_count = {}
        for word in words:
            length = len(word)
            length_count[length] = length_count.get(length, 0) + 1
            
        stats["word_length_distribution"] = dict(sorted(length_count.items()))
        
        # 统计源文件
        if os.path.exists(self.vocabulary_dir):
            for filename in os.listdir(self.vocabulary_dir):
                if filename.endswith('.txt'):
                    stats["source_files"].append(filename)
                    
        return stats
        
    def run(self) -> bool:
        """
        运行修复程序
        
        Returns:
            bool: 是否成功完成修复
        """
        logger.info("开始修复敏感词库JSON格式...")
        start_time = datetime.now()
        
        try:
            # 读取所有词汇文件
            words = self.read_vocabulary_files()
            
            if not words:
                logger.error("没有读取到任何词汇，修复失败")
                return False
                
            # 创建合并的txt文件
            if not self.create_merged_txt(words):
                logger.error("创建txt文件失败")
                return False
                
            # 创建合并的JSON文件
            if not self.create_merged_json(words):
                logger.error("创建JSON文件失败")
                return False
                
            # 生成并显示统计信息
            stats = self.generate_statistics(words)
            logger.info("=== 修复统计信息 ===")
            logger.info(f"总词汇数: {stats['total_words']}")
            logger.info(f"源文件数: {len(stats['source_files'])}")
            logger.info(f"生成时间: {stats['generation_time']}")
            
            # 显示词汇长度分布（前10个）
            logger.info("词汇长度分布（前10个）:")
            for length, count in list(stats['word_length_distribution'].items())[:10]:
                logger.info(f"  长度 {length}: {count} 个词汇")
                
            end_time = datetime.now()
            duration = end_time - start_time
            logger.info(f"修复完成！耗时: {duration}")
            
            return True
            
        except Exception as e:
            logger.error(f"修复过程中出现错误: {e}", exc_info=True)
            return False


def main():
    """主函数"""
    print("=" * 60)
    print("敏感词库JSON格式修复工具")
    print("Sensitive Words JSON Format Fixer")
    print("=" * 60)
    
    fixer = SensitiveWordsJSONFixer()
    success = fixer.run()
    
    if success:
        print("✅ JSON格式修复任务完成!")
        print(f"📁 输出文件:")
        print(f"   - {fixer.output_txt}")
        print(f"   - {fixer.output_json}")
        print("📊 修复内容:")
        print("   - 处理逗号分隔的词汇行")
        print("   - 去除词汇前后空白字符")
        print("   - 确保JSON格式正确")
        print("   - 支持UTF-8编码中文字符")
        print("   - 更新词汇总数统计")
    else:
        print("❌ 修复任务失败，请查看日志了解详情")
        return 1
        
    return 0


if __name__ == '__main__':
    exit(main())