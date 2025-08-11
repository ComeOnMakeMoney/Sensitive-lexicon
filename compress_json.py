#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JSON文件压缩脚本
JSON File Compression Script

该脚本用于压缩merged_sensitive_words.json文件，优化文件大小，
同时保持数据完整性和JSON格式的有效性。
"""

import os
import json
import gzip
import shutil
import logging
from datetime import datetime
from typing import Dict, Any, Tuple

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class JSONCompressor:
    """JSON压缩器"""
    
    def __init__(self):
        """初始化压缩器"""
        self.compression_stats = {}
    
    def get_file_size(self, filepath: str) -> int:
        """获取文件大小
        
        Args:
            filepath: 文件路径
            
        Returns:
            文件大小（字节）
        """
        return os.path.getsize(filepath) if os.path.exists(filepath) else 0
    
    def format_size(self, size_bytes: int) -> str:
        """格式化文件大小显示
        
        Args:
            size_bytes: 字节数
            
        Returns:
            格式化的大小字符串
        """
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        else:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
    
    def validate_json_integrity(self, original_file: str, compressed_file: str) -> bool:
        """验证压缩后JSON的完整性
        
        Args:
            original_file: 原始文件路径
            compressed_file: 压缩文件路径
            
        Returns:
            是否完整
        """
        try:
            # 读取原始文件
            with open(original_file, 'r', encoding='utf-8') as f:
                original_data = json.load(f)
            
            # 读取压缩文件
            with open(compressed_file, 'r', encoding='utf-8') as f:
                compressed_data = json.load(f)
            
            # 比较关键字段
            if original_data.get('totalCount') != compressed_data.get('totalCount'):
                logger.error("词汇总数不匹配")
                return False
            
            if len(original_data.get('words', [])) != len(compressed_data.get('words', [])):
                logger.error("词汇列表长度不匹配")
                return False
            
            # 比较词汇内容（排序后比较以避免顺序问题）
            original_words = sorted(original_data.get('words', []))
            compressed_words = sorted(compressed_data.get('words', []))
            
            if original_words != compressed_words:
                logger.error("词汇内容不匹配")
                return False
            
            logger.info("✅ 数据完整性验证通过")
            return True
            
        except Exception as e:
            logger.error(f"❌ 完整性验证失败: {e}")
            return False
    
    def compress_json_format(self, input_file: str, output_file: str) -> Tuple[int, int]:
        """压缩JSON格式（移除空白字符）
        
        Args:
            input_file: 输入文件路径
            output_file: 输出文件路径
            
        Returns:
            (原始大小, 压缩后大小)
        """
        try:
            # 读取JSON数据
            with open(input_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 以紧凑格式保存（无缩进，无空格）
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
            
            original_size = self.get_file_size(input_file)
            compressed_size = self.get_file_size(output_file)
            
            return original_size, compressed_size
            
        except Exception as e:
            logger.error(f"❌ JSON格式压缩失败: {e}")
            raise
    
    def create_gzip_version(self, input_file: str, output_file: str) -> int:
        """创建GZIP压缩版本
        
        Args:
            input_file: 输入文件路径
            output_file: 输出文件路径（.gz文件）
            
        Returns:
            压缩后大小
        """
        try:
            with open(input_file, 'rb') as f_in:
                with gzip.open(output_file, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            
            return self.get_file_size(output_file)
            
        except Exception as e:
            logger.error(f"❌ GZIP压缩失败: {e}")
            raise
    
    def compress_file(self, input_file: str) -> Dict[str, Any]:
        """压缩文件并生成统计信息
        
        Args:
            input_file: 输入文件路径
            
        Returns:
            压缩统计信息
        """
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"输入文件不存在: {input_file}")
        
        logger.info(f"开始压缩文件: {input_file}")
        
        # 生成输出文件名
        base_name = os.path.splitext(input_file)[0]
        compressed_file = f"{base_name}_compressed.json"
        gzip_file = f"{base_name}_compressed.json.gz"
        
        # 获取原始文件大小
        original_size = self.get_file_size(input_file)
        logger.info(f"📁 原始文件大小: {self.format_size(original_size)}")
        
        # 执行JSON格式压缩
        logger.info("🗜️ 执行JSON格式压缩...")
        original_size, compressed_size = self.compress_json_format(input_file, compressed_file)
        
        # 创建GZIP版本
        logger.info("🗜️ 创建GZIP压缩版本...")
        gzip_size = self.create_gzip_version(compressed_file, gzip_file)
        
        # 验证数据完整性
        logger.info("🔍 验证数据完整性...")
        if not self.validate_json_integrity(input_file, compressed_file):
            raise Exception("数据完整性验证失败")
        
        # 计算压缩比例
        json_compression_ratio = (1 - compressed_size / original_size) * 100
        gzip_compression_ratio = (1 - gzip_size / original_size) * 100
        
        # 生成统计信息
        stats = {
            "timestamp": datetime.now().isoformat(),
            "original_file": input_file,
            "original_size": original_size,
            "original_size_formatted": self.format_size(original_size),
            "compressed_file": compressed_file,
            "compressed_size": compressed_size,
            "compressed_size_formatted": self.format_size(compressed_size),
            "gzip_file": gzip_file,
            "gzip_size": gzip_size,
            "gzip_size_formatted": self.format_size(gzip_size),
            "json_compression_ratio": json_compression_ratio,
            "gzip_compression_ratio": gzip_compression_ratio,
            "space_saved_json": original_size - compressed_size,
            "space_saved_gzip": original_size - gzip_size
        }
        
        self.compression_stats = stats
        return stats
    
    def print_compression_report(self, stats: Dict[str, Any]):
        """打印压缩报告
        
        Args:
            stats: 压缩统计信息
        """
        print("\n" + "="*60)
        print("📊 JSON文件压缩报告")
        print("="*60)
        print(f"🕐 压缩时间: {stats['timestamp']}")
        print(f"📄 原始文件: {stats['original_file']}")
        print(f"📁 原始大小: {stats['original_size_formatted']} ({stats['original_size']:,} 字节)")
        print()
        print("🗜️ JSON格式压缩结果:")
        print(f"  📄 压缩文件: {stats['compressed_file']}")
        print(f"  📁 压缩大小: {stats['compressed_size_formatted']} ({stats['compressed_size']:,} 字节)")
        print(f"  📉 压缩比例: {stats['json_compression_ratio']:.1f}%")
        print(f"  💾 节省空间: {self.format_size(stats['space_saved_json'])}")
        print()
        print("🗜️ GZIP压缩结果:")
        print(f"  📄 压缩文件: {stats['gzip_file']}")
        print(f"  📁 压缩大小: {stats['gzip_size_formatted']} ({stats['gzip_size']:,} 字节)")
        print(f"  📉 压缩比例: {stats['gzip_compression_ratio']:.1f}%")
        print(f"  💾 节省空间: {self.format_size(stats['space_saved_gzip'])}")
        print()
        print("💡 使用建议:")
        if stats['json_compression_ratio'] > 30:
            print("  ✅ JSON格式压缩效果显著，建议使用压缩版本")
        else:
            print("  ⚠️ JSON格式压缩效果一般")
        
        if stats['gzip_compression_ratio'] > 50:
            print("  ✅ GZIP压缩效果优秀，适合存储和传输")
        else:
            print("  ⚠️ GZIP压缩效果一般")
        print("="*60)
    
    def save_compression_report(self, stats: Dict[str, Any], report_file: str = "compression_report.json"):
        """保存压缩报告到文件
        
        Args:
            stats: 压缩统计信息
            report_file: 报告文件路径
        """
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(stats, f, ensure_ascii=False, indent=2)
            logger.info(f"📋 压缩报告已保存到: {report_file}")
        except Exception as e:
            logger.error(f"❌ 保存报告失败: {e}")

def main():
    """主函数"""
    import sys
    
    # 默认输入文件
    input_file = "merged_sensitive_words.json"
    
    # 检查命令行参数
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    
    # 检查输入文件是否存在
    if not os.path.exists(input_file):
        logger.error(f"❌ 输入文件不存在: {input_file}")
        logger.info("请先运行 generate_merged_json.py 生成合并文件")
        return
    
    # 创建压缩器并执行压缩
    compressor = JSONCompressor()
    
    try:
        # 执行压缩
        stats = compressor.compress_file(input_file)
        
        # 打印报告
        compressor.print_compression_report(stats)
        
        # 保存报告
        compressor.save_compression_report(stats)
        
        logger.info("🎉 压缩任务完成！")
        
    except Exception as e:
        logger.error(f"❌ 压缩过程中出错: {e}")

if __name__ == "__main__":
    main()