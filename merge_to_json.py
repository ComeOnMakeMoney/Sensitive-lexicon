#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
敏感词库合并和JSON转换脚本
Sensitive Lexicon Merging and JSON Conversion Script

该脚本用于：
1. 将Vocabulary文件夹中的所有敏感词库文件合并到merged_sensitive_words.txt
2. 将merged_sensitive_words.txt转换为JSON格式
"""

import os
import json
import re
import logging
from datetime import datetime
from typing import Set, List, Dict, Any

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('merge_to_json.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class SensitiveWordMerger:
    """敏感词合并和JSON转换器"""
    
    def __init__(self):
        """初始化转换器"""
        self.vocabulary_dir = "Vocabulary"
        self.merged_file = "merged_sensitive_words.txt"
        self.json_file = "merged_sensitive_words.json"
    
    def read_vocabulary_files(self) -> Set[str]:
        """读取并合并所有词汇文件"""
        logger.info("开始读取词汇文件...")
        all_words = set()
        
        if not os.path.exists(self.vocabulary_dir):
            logger.error(f"词汇目录 {self.vocabulary_dir} 不存在")
            return all_words
        
        file_count = 0
        total_words_read = 0
        
        for filename in os.listdir(self.vocabulary_dir):
            if filename.endswith('.txt'):
                filepath = os.path.join(self.vocabulary_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                        # 处理不同的分隔符
                        if '\n' in content:
                            words = content.split('\n')
                        else:
                            # 处理可能的空格或其他分隔符
                            words = re.split(r'[\s,，、]+', content)
                        
                        # 清理词汇
                        file_words = 0
                        for word in words:
                            word = word.strip()
                            # 跳过注释行、空行和空白字符
                            if word and not word.startswith('#') and len(word) > 0:
                                all_words.add(word)
                                file_words += 1
                        
                        total_words_read += file_words
                        file_count += 1
                        logger.info(f"读取文件 {filename}: {file_words} 个词汇")
                        
                except Exception as e:
                    logger.error(f"读取文件 {filename} 失败: {e}")
        
        logger.info(f"总计读取 {file_count} 个文件，{total_words_read} 个原始词汇，去重后 {len(all_words)} 个词汇")
        return all_words
    
    def create_merged_file(self, words: Set[str]) -> bool:
        """创建合并的敏感词文件"""
        logger.info(f"创建合并文件 {self.merged_file}...")
        
        try:
            # 按字母顺序排序
            sorted_words = sorted(list(words))
            
            with open(self.merged_file, 'w', encoding='utf-8') as f:
                # 添加文件头注释
                f.write(f"# 敏感词库合并文件\n")
                f.write(f"# 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"# 总词汇数: {len(sorted_words)}\n")
                f.write(f"# 来源: Vocabulary目录下的所有.txt文件\n")
                f.write(f"#\n")
                
                # 写入所有词汇
                for word in sorted_words:
                    f.write(word + '\n')
            
            logger.info(f"成功创建 {self.merged_file}，包含 {len(sorted_words)} 个词汇")
            return True
            
        except Exception as e:
            logger.error(f"创建合并文件失败: {e}")
            return False
    
    def read_merged_file(self) -> List[str]:
        """读取合并文件中的词汇"""
        logger.info(f"读取合并文件 {self.merged_file}...")
        words = []
        
        if not os.path.exists(self.merged_file):
            logger.error(f"合并文件 {self.merged_file} 不存在")
            return words
        
        try:
            with open(self.merged_file, 'r', encoding='utf-8') as f:
                for line in f:
                    word = line.strip()
                    # 跳过注释行和空行
                    if word and not word.startswith('#'):
                        words.append(word)
            
            logger.info(f"从合并文件读取到 {len(words)} 个词汇")
            return words
            
        except Exception as e:
            logger.error(f"读取合并文件失败: {e}")
            return words
    
    def create_json_file(self, words: List[str]) -> bool:
        """创建JSON格式文件"""
        logger.info(f"创建JSON文件 {self.json_file}...")
        
        try:
            # 创建JSON数据结构
            json_data = {
                "metadata": {
                    "source_file": self.merged_file,
                    "converted_time": datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
                    "total_words": len(words),
                    "description": "敏感词库 - 所有词汇的简单列表"
                },
                "words": words
            }
            
            # 写入JSON文件，确保支持中文字符
            with open(self.json_file, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"成功创建 {self.json_file}，包含 {len(words)} 个词汇")
            return True
            
        except Exception as e:
            logger.error(f"创建JSON文件失败: {e}")
            return False
    
    def validate_json_file(self) -> bool:
        """验证JSON文件格式正确性"""
        logger.info("验证JSON文件格式...")
        
        try:
            with open(self.json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 验证基本结构
            if 'metadata' not in data or 'words' not in data:
                logger.error("JSON文件缺少必要的字段")
                return False
            
            # 验证metadata字段
            required_fields = ['source_file', 'converted_time', 'total_words', 'description']
            for field in required_fields:
                if field not in data['metadata']:
                    logger.error(f"metadata缺少字段: {field}")
                    return False
            
            # 验证词汇数量
            if data['metadata']['total_words'] != len(data['words']):
                logger.error("词汇数量不匹配")
                return False
            
            logger.info("JSON文件格式验证通过")
            return True
            
        except Exception as e:
            logger.error(f"JSON文件格式验证失败: {e}")
            return False
    
    def run(self) -> bool:
        """运行完整的合并和转换流程"""
        logger.info("开始敏感词库合并和JSON转换任务...")
        start_time = datetime.now()
        
        try:
            # 步骤1: 读取并合并所有词汇文件
            all_words = self.read_vocabulary_files()
            if not all_words:
                logger.error("没有读取到任何词汇")
                return False
            
            # 步骤2: 创建合并文件
            if not self.create_merged_file(all_words):
                logger.error("创建合并文件失败")
                return False
            
            # 步骤3: 从合并文件读取词汇
            words = self.read_merged_file()
            if not words:
                logger.error("从合并文件读取词汇失败")
                return False
            
            # 步骤4: 创建JSON文件
            if not self.create_json_file(words):
                logger.error("创建JSON文件失败")
                return False
            
            # 步骤5: 验证JSON文件
            if not self.validate_json_file():
                logger.error("JSON文件验证失败")
                return False
            
            end_time = datetime.now()
            duration = end_time - start_time
            
            logger.info(f"任务完成! 耗时: {duration}")
            logger.info(f"生成文件: {self.merged_file}, {self.json_file}")
            
            return True
            
        except Exception as e:
            logger.error(f"任务执行失败: {e}", exc_info=True)
            return False


def main():
    """主函数"""
    merger = SensitiveWordMerger()
    success = merger.run()
    
    if success:
        print("✅ 敏感词库合并和JSON转换任务完成!")
        print(f"📁 生成文件: {merger.merged_file}")
        print(f"📄 生成文件: {merger.json_file}")
    else:
        print("❌ 任务执行失败，请查看日志了解详情")
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())