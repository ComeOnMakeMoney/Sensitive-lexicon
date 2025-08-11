#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JSON文件验证工具
JSON File Validation Tool

验证压缩后JSON文件的完整性和有效性
"""

import os
import json
import gzip
import logging
from typing import Dict, Any, List, Tuple

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class JSONValidator:
    """JSON验证器"""
    
    def __init__(self):
        """初始化验证器"""
        self.validation_results = {}
    
    def load_json_file(self, filepath: str) -> Dict[str, Any]:
        """加载JSON文件
        
        Args:
            filepath: 文件路径
            
        Returns:
            JSON数据
        """
        try:
            if filepath.endswith('.gz'):
                with gzip.open(filepath, 'rt', encoding='utf-8') as f:
                    return json.load(f)
            else:
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"❌ 加载文件 {filepath} 失败: {e}")
            raise
    
    def validate_structure(self, data: Dict[str, Any], filename: str) -> List[str]:
        """验证JSON结构
        
        Args:
            data: JSON数据
            filename: 文件名
            
        Returns:
            错误列表
        """
        errors = []
        
        # 检查必要字段
        required_fields = ['lastUpdateDate', 'totalCount', 'words']
        for field in required_fields:
            if field not in data:
                errors.append(f"缺少必要字段: {field}")
        
        # 检查可选字段
        optional_fields = ['description', 'categories']
        for field in optional_fields:
            if field not in data:
                logger.info(f"📝 {filename}: 缺少可选字段 {field}")
        
        # 验证数据类型
        if 'totalCount' in data and not isinstance(data['totalCount'], int):
            errors.append("totalCount字段必须是整数")
        
        if 'words' in data and not isinstance(data['words'], list):
            errors.append("words字段必须是列表")
        
        if 'lastUpdateDate' in data and not isinstance(data['lastUpdateDate'], str):
            errors.append("lastUpdateDate字段必须是字符串")
        
        return errors
    
    def validate_data_consistency(self, data: Dict[str, Any]) -> List[str]:
        """验证数据一致性
        
        Args:
            data: JSON数据
            
        Returns:
            错误列表
        """
        errors = []
        
        if 'totalCount' in data and 'words' in data:
            declared_count = data['totalCount']
            actual_count = len(data['words'])
            
            if declared_count != actual_count:
                errors.append(f"词汇数量不匹配: 声明 {declared_count}, 实际 {actual_count}")
        
        # 检查重复词汇
        if 'words' in data:
            words = data['words']
            unique_words = set(words)
            duplicate_count = len(words) - len(unique_words)
            
            if duplicate_count > 0:
                errors.append(f"发现 {duplicate_count} 个重复词汇")
        
        # 检查空词汇
        if 'words' in data:
            empty_words = [i for i, word in enumerate(data['words']) if not word or not word.strip()]
            if empty_words:
                errors.append(f"发现 {len(empty_words)} 个空词汇，位置: {empty_words[:10]}")
        
        return errors
    
    def validate_file(self, filepath: str) -> Dict[str, Any]:
        """验证单个文件
        
        Args:
            filepath: 文件路径
            
        Returns:
            验证结果
        """
        result = {
            'file': filepath,
            'exists': os.path.exists(filepath),
            'valid_json': False,
            'structure_errors': [],
            'data_errors': [],
            'word_count': 0,
            'file_size': 0
        }
        
        if not result['exists']:
            result['structure_errors'].append("文件不存在")
            return result
        
        result['file_size'] = os.path.getsize(filepath)
        
        try:
            # 加载JSON数据
            data = self.load_json_file(filepath)
            result['valid_json'] = True
            
            # 验证结构
            result['structure_errors'] = self.validate_structure(data, filepath)
            
            # 验证数据一致性
            result['data_errors'] = self.validate_data_consistency(data)
            
            # 获取词汇数量
            if 'words' in data:
                result['word_count'] = len(data['words'])
            
        except json.JSONDecodeError as e:
            result['structure_errors'].append(f"JSON格式错误: {e}")
        except Exception as e:
            result['structure_errors'].append(f"其他错误: {e}")
        
        return result
    
    def compare_files(self, file1: str, file2: str) -> Dict[str, Any]:
        """比较两个文件的内容
        
        Args:
            file1: 第一个文件路径
            file2: 第二个文件路径
            
        Returns:
            比较结果
        """
        comparison = {
            'files': [file1, file2],
            'identical': False,
            'word_count_match': False,
            'content_match': False,
            'differences': []
        }
        
        try:
            data1 = self.load_json_file(file1)
            data2 = self.load_json_file(file2)
            
            # 比较词汇数量
            count1 = len(data1.get('words', []))
            count2 = len(data2.get('words', []))
            comparison['word_count_match'] = count1 == count2
            
            if not comparison['word_count_match']:
                comparison['differences'].append(f"词汇数量不同: {count1} vs {count2}")
            
            # 比较词汇内容
            words1 = set(data1.get('words', []))
            words2 = set(data2.get('words', []))
            comparison['content_match'] = words1 == words2
            
            if not comparison['content_match']:
                only_in_1 = words1 - words2
                only_in_2 = words2 - words1
                
                if only_in_1:
                    comparison['differences'].append(f"仅在 {file1} 中: {len(only_in_1)} 个词汇")
                if only_in_2:
                    comparison['differences'].append(f"仅在 {file2} 中: {len(only_in_2)} 个词汇")
            
            comparison['identical'] = comparison['word_count_match'] and comparison['content_match']
            
        except Exception as e:
            comparison['differences'].append(f"比较失败: {e}")
        
        return comparison
    
    def print_validation_report(self, results: List[Dict[str, Any]]):
        """打印验证报告
        
        Args:
            results: 验证结果列表
        """
        print("\n" + "="*70)
        print("🔍 JSON文件验证报告")
        print("="*70)
        
        for result in results:
            print(f"\n📄 文件: {result['file']}")
            print(f"   📁 大小: {result['file_size']:,} 字节")
            
            if not result['exists']:
                print("   ❌ 文件不存在")
                continue
            
            if result['valid_json']:
                print("   ✅ JSON格式有效")
                print(f"   📊 词汇数量: {result['word_count']:,}")
            else:
                print("   ❌ JSON格式无效")
            
            if result['structure_errors']:
                print("   ⚠️ 结构错误:")
                for error in result['structure_errors']:
                    print(f"      - {error}")
            
            if result['data_errors']:
                print("   ⚠️ 数据错误:")
                for error in result['data_errors']:
                    print(f"      - {error}")
            
            if not result['structure_errors'] and not result['data_errors']:
                print("   ✅ 验证通过")
        
        print("="*70)
    
    def validate_compression_files(self) -> bool:
        """验证压缩相关的所有文件
        
        Returns:
            是否全部验证通过
        """
        files_to_validate = [
            'merged_sensitive_words.json',
            'merged_sensitive_words_compressed.json',
            'merged_sensitive_words_compressed.json.gz'
        ]
        
        results = []
        all_valid = True
        
        # 验证每个文件
        for filepath in files_to_validate:
            result = self.validate_file(filepath)
            results.append(result)
            
            has_errors = bool(result['structure_errors'] or result['data_errors'])
            if not result['exists'] or not result['valid_json'] or has_errors:
                all_valid = False
        
        # 打印验证报告
        self.print_validation_report(results)
        
        # 比较文件内容
        if len(results) >= 2:
            print("\n🔄 文件内容比较:")
            
            # 比较原始和压缩版本
            if results[0]['valid_json'] and results[1]['valid_json']:
                comparison = self.compare_files(
                    'merged_sensitive_words.json',
                    'merged_sensitive_words_compressed.json'
                )
                
                if comparison['identical']:
                    print("   ✅ 原始文件与JSON压缩版本内容一致")
                else:
                    print("   ❌ 原始文件与JSON压缩版本内容不一致")
                    for diff in comparison['differences']:
                        print(f"      - {diff}")
                    all_valid = False
            
            # 比较JSON压缩和GZIP版本
            if results[1]['valid_json'] and results[2]['valid_json']:
                comparison = self.compare_files(
                    'merged_sensitive_words_compressed.json',
                    'merged_sensitive_words_compressed.json.gz'
                )
                
                if comparison['identical']:
                    print("   ✅ JSON压缩版本与GZIP版本内容一致")
                else:
                    print("   ❌ JSON压缩版本与GZIP版本内容不一致")
                    for diff in comparison['differences']:
                        print(f"      - {diff}")
                    all_valid = False
        
        return all_valid

def main():
    """主函数"""
    validator = JSONValidator()
    
    logger.info("开始验证JSON压缩文件...")
    
    try:
        all_valid = validator.validate_compression_files()
        
        if all_valid:
            logger.info("🎉 所有文件验证通过！")
        else:
            logger.error("❌ 部分文件验证失败")
            return False
        
    except Exception as e:
        logger.error(f"❌ 验证过程中出错: {e}")
        return False
    
    return True

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)