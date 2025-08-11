#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动化压缩流水线
Automated Compression Pipeline

一键完成从词汇分类到JSON压缩的完整流程
"""

import os
import sys
import time
import logging
import subprocess
from typing import Dict, Any

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class CompressionPipeline:
    """压缩流水线"""
    
    def __init__(self):
        """初始化流水线"""
        self.start_time = time.time()
        self.steps_completed = 0
        self.total_steps = 4
    
    def print_banner(self):
        """打印横幅"""
        print("\n" + "="*80)
        print("🚀 敏感词库JSON压缩自动化流水线")
        print("   Sensitive Lexicon JSON Compression Automated Pipeline")
        print("="*80)
        print()
    
    def print_step(self, step_num: int, title: str):
        """打印步骤信息"""
        print(f"📋 步骤 {step_num}/{self.total_steps}: {title}")
        print("-" * 50)
    
    def run_script(self, script_name: str, description: str) -> bool:
        """运行Python脚本
        
        Args:
            script_name: 脚本文件名
            description: 脚本描述
            
        Returns:
            是否成功
        """
        try:
            logger.info(f"开始运行: {description}")
            result = subprocess.run(
                [sys.executable, script_name],
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            
            if result.returncode == 0:
                logger.info(f"✅ {description} 完成")
                return True
            else:
                logger.error(f"❌ {description} 失败")
                if result.stderr:
                    logger.error(f"错误信息: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"❌ 运行 {script_name} 时出错: {e}")
            return False
    
    def check_prerequisites(self) -> bool:
        """检查先决条件
        
        Returns:
            是否满足条件
        """
        required_files = [
            'classify_vocabulary.py',
            'generate_merged_json.py', 
            'compress_json.py'
        ]
        
        missing_files = []
        for file in required_files:
            if not os.path.exists(file):
                missing_files.append(file)
        
        if missing_files:
            logger.error(f"❌ 缺少必要文件: {', '.join(missing_files)}")
            return False
        
        # 检查Vocabulary目录
        if not os.path.exists('Vocabulary'):
            logger.error("❌ Vocabulary目录不存在")
            return False
        
        return True
    
    def get_file_sizes(self) -> Dict[str, int]:
        """获取关键文件的大小
        
        Returns:
            文件大小字典
        """
        files = {
            'merged_sensitive_words.json': 0,
            'merged_sensitive_words_compressed.json': 0,
            'merged_sensitive_words_compressed.json.gz': 0
        }
        
        for filename in files:
            if os.path.exists(filename):
                files[filename] = os.path.getsize(filename)
        
        return files
    
    def format_size(self, size_bytes: int) -> str:
        """格式化文件大小"""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        else:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
    
    def print_final_report(self):
        """打印最终报告"""
        end_time = time.time()
        duration = end_time - self.start_time
        
        # 获取文件大小
        file_sizes = self.get_file_sizes()
        
        print("\n" + "="*80)
        print("📊 压缩流水线完成报告")
        print("="*80)
        print(f"⏱️ 总耗时: {duration:.2f} 秒")
        print(f"✅ 完成步骤: {self.steps_completed}/{self.total_steps}")
        print()
        
        if file_sizes['merged_sensitive_words.json'] > 0:
            original_size = file_sizes['merged_sensitive_words.json']
            compressed_size = file_sizes['merged_sensitive_words_compressed.json'] 
            gzip_size = file_sizes['merged_sensitive_words_compressed.json.gz']
            
            print("📁 生成文件大小:")
            print(f"  📄 原始文件: {self.format_size(original_size)}")
            
            if compressed_size > 0:
                compression_ratio = (1 - compressed_size / original_size) * 100
                print(f"  🗜️ JSON压缩: {self.format_size(compressed_size)} ({compression_ratio:.1f}% 压缩)")
            
            if gzip_size > 0:
                gzip_ratio = (1 - gzip_size / original_size) * 100
                print(f"  🗜️ GZIP压缩: {self.format_size(gzip_size)} ({gzip_ratio:.1f}% 压缩)")
        
        print("\n📂 生成的文件:")
        for filename, size in file_sizes.items():
            if size > 0:
                print(f"  ✅ {filename} ({self.format_size(size)})")
        
        print("\n💡 使用建议:")
        print("  - 开发环境: 使用 merged_sensitive_words.json")
        print("  - 生产环境: 使用 merged_sensitive_words_compressed.json") 
        print("  - 存储传输: 使用 merged_sensitive_words_compressed.json.gz")
        print("="*80)
    
    def run(self) -> bool:
        """运行完整流水线
        
        Returns:
            是否成功
        """
        self.print_banner()
        
        # 步骤1: 检查先决条件
        self.print_step(1, "检查先决条件")
        if not self.check_prerequisites():
            logger.error("❌ 先决条件检查失败")
            return False
        logger.info("✅ 先决条件检查通过")
        self.steps_completed += 1
        print()
        
        # 步骤2: 词汇分类
        self.print_step(2, "执行词汇分类")
        if not self.run_script('classify_vocabulary.py', '词汇分类'):
            logger.error("❌ 词汇分类失败")
            return False
        self.steps_completed += 1
        print()
        
        # 步骤3: 生成合并JSON
        self.print_step(3, "生成合并JSON文件")
        if not self.run_script('generate_merged_json.py', '生成合并JSON'):
            logger.error("❌ 生成合并JSON失败")
            return False
        self.steps_completed += 1
        print()
        
        # 步骤4: 压缩JSON
        self.print_step(4, "压缩JSON文件")
        if not self.run_script('compress_json.py', 'JSON压缩'):
            logger.error("❌ JSON压缩失败")
            return False
        self.steps_completed += 1
        print()
        
        # 打印最终报告
        self.print_final_report()
        
        logger.info("🎉 压缩流水线成功完成！")
        return True

def main():
    """主函数"""
    pipeline = CompressionPipeline()
    
    try:
        success = pipeline.run()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        logger.info("⚠️ 用户中断操作")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ 流水线执行出错: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()