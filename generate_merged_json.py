#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成合并的敏感词JSON文件
Generate Merged Sensitive Words JSON File

该脚本从分类后的敏感词库文件生成一个包含所有词汇的JSON文件，
包含适当的元数据信息。
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Set

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MergedJSONGenerator:
    """合并JSON生成器"""
    
    def __init__(self, classified_dir: str = "classified_vocabulary"):
        """初始化生成器
        
        Args:
            classified_dir: 分类词库目录
        """
        self.classified_dir = classified_dir
        self.categories = ['political', 'pornographic', 'violent', 'gambling', 'advertising', 'others']
        
    def load_all_words(self) -> List[str]:
        """加载所有分类的敏感词
        
        Returns:
            所有敏感词的列表
        """
        all_words = set()
        
        for category in self.categories:
            filename = f"{category}.txt"
            filepath = os.path.join(self.classified_dir, filename)
            
            if os.path.exists(filepath):
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        words = {line.strip() for line in f if line.strip()}
                        all_words.update(words)
                        logger.info(f"加载 {category}: {len(words)} 个词汇")
                except Exception as e:
                    logger.warning(f"读取文件 {filepath} 时出错: {e}")
            else:
                logger.warning(f"文件不存在: {filepath}")
        
        # 转换为排序的列表
        return sorted(list(all_words))
    
    def generate_merged_json(self, output_path: str = "merged_sensitive_words.json") -> Dict:
        """生成合并的JSON文件
        
        Args:
            output_path: 输出文件路径
            
        Returns:
            生成的JSON数据
        """
        logger.info("开始生成合并的敏感词JSON文件...")
        
        # 加载所有词汇
        all_words = self.load_all_words()
        total_words = len(all_words)
        
        # 创建JSON数据结构
        merged_data = {
            "lastUpdateDate": datetime.now().strftime("%Y/%m/%d"),
            "totalCount": total_words,
            "description": "合并后的敏感词库，包含政治类、色情类、暴力类、赌博类、广告类等多种类型的敏感词汇",
            "categories": {
                "political": "政治类",
                "pornographic": "色情类",
                "violent": "暴力类",
                "gambling": "赌博类",
                "advertising": "广告类",
                "others": "其他类"
            },
            "words": all_words
        }
        
        # 保存JSON文件
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(merged_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"✅ 成功生成合并文件: {output_path}")
            logger.info(f"📊 总词汇数量: {total_words}")
            
            # 显示文件大小
            file_size = os.path.getsize(output_path)
            logger.info(f"📁 文件大小: {file_size:,} 字节 ({file_size/1024:.1f} KB)")
            
            return merged_data
            
        except Exception as e:
            logger.error(f"❌ 保存文件时出错: {e}")
            raise
    
    def validate_json(self, filepath: str) -> bool:
        """验证JSON文件的有效性
        
        Args:
            filepath: JSON文件路径
            
        Returns:
            是否有效
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 检查必要字段
            required_fields = ['lastUpdateDate', 'totalCount', 'words']
            for field in required_fields:
                if field not in data:
                    logger.error(f"❌ 缺少必要字段: {field}")
                    return False
            
            # 检查词汇数量是否匹配
            actual_count = len(data['words'])
            declared_count = data['totalCount']
            
            if actual_count != declared_count:
                logger.error(f"❌ 词汇数量不匹配: 声明 {declared_count}, 实际 {actual_count}")
                return False
            
            logger.info("✅ JSON文件验证通过")
            return True
            
        except json.JSONDecodeError as e:
            logger.error(f"❌ JSON格式错误: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ 验证时出错: {e}")
            return False

def main():
    """主函数"""
    generator = MergedJSONGenerator()
    
    # 检查分类目录是否存在
    if not os.path.exists(generator.classified_dir):
        logger.error(f"❌ 分类目录不存在: {generator.classified_dir}")
        logger.info("请先运行 classify_vocabulary.py 生成分类文件")
        return
    
    # 生成合并JSON文件
    try:
        merged_data = generator.generate_merged_json()
        
        # 验证生成的文件
        if generator.validate_json("merged_sensitive_words.json"):
            logger.info("🎉 合并JSON文件生成成功！")
        else:
            logger.error("❌ 生成的JSON文件验证失败")
            
    except Exception as e:
        logger.error(f"❌ 生成过程中出错: {e}")

if __name__ == "__main__":
    main()