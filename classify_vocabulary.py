#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
敏感词库合并和分类脚本
Sensitive Lexicon Merging and Classification Script

该脚本用于处理Vocabulary文件夹中的所有敏感词库文件，
进行合并、去重、分类和整理。
"""

import os
import re
import logging
from datetime import datetime
from collections import defaultdict, Counter
from typing import Dict, List, Set, Tuple

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('classify_vocabulary.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SensitiveWordClassifier:
    """敏感词分类器"""
    
    def __init__(self):
        """初始化分类器"""
        self.vocabulary_dir = "Vocabulary"
        self.output_dir = "classified_vocabulary"
        self.categories = {
            'political': '政治类',
            'pornographic': '色情类', 
            'violent': '暴力类',
            'gambling': '赌博类',
            'advertising': '广告类',
            'others': '其他类'
        }
        
        # 分类关键词模式
        self.political_patterns = [
            # 政治人物
            r'(习|胡|江|温|李|朱|邓|毛|周|刘|彭|林|陈|贺|聂|徐|罗|叶).*(平|锦|泽|家|鹏|镕|小|泽|恩|少|德|彪|伯|毅|龙|荣|向|桓|剑)',
            # 政治词汇
            r'.*(共产|社会主义|民主|自由|独立|分裂|颠覆|反动|政府|政治|党|主席|总理|书记)',
            r'.*(打倒|推翻|抵制|反对).*(中国|共产|政府|党)',
            r'.*(台独|藏独|疆独|港独)',
            r'.*(法轮|轮功|大法)',
            r'(64|六四|天安门|广场)',
            r'.*(民运|学运|游行|示威|抗议)',
        ]
        
        self.pornographic_patterns = [
            r'.*(性|色|情|淫|奸|操|干|插|草|屌|鸡|逼|屄|妓|嫖|春)',
            r'.*(爱液|按摩棒|暴乳|乳房|阴|精液|高潮|做爱|性交)',
            r'.*(A片|黄片|色情|成人|裸|脱|露)',
        ]
        
        self.violent_patterns = [
            r'.*(杀|死|血|暴|恐|炸|枪|刀|毒|打|砍|爆|屠|虐)',
            r'.*(自杀|他杀|谋杀|暴力|恐怖|爆炸|袭击)',
            r'.*(ISIS|基地组织|恐怖分子)',
        ]
        
        self.gambling_patterns = [
            r'.*(赌|博|彩票|老虎机|百家乐|21点|轮盘|骰子)',
            r'.*(澳门|拉斯维加斯|赌场|庄家|下注|押注)',
            r'.*(六合彩|时时彩|快三|PK10)',
        ]
        
        self.advertising_patterns = [
            r'.*(办证|办理|代办|包过|保过|快速|低价|优惠|促销)',
            r'.*(贷款|借钱|信用卡|pos机|刷卡|套现)',
            r'.*(发票|票据|证书|文凭|学历|资格证)',
            r'.*(减肥|丰胸|美容|整形|药品|保健品)',
            r'.*(兼职|招聘|网赚|刷单|点击|推广)',
            # 网站和域名相关
            r'.*\.(com|cn|net|org|info|biz|tv|cc|tk|ml|ga|cf|gq)',
            r'.*www\.|.*http|.*ftp',
            r'.*qq.*\d+.*\..*',  # QQ相关网站
            r'\d{3,4}\.\w+\.\w+',  # 数字开头的域名
        ]

    def read_vocabulary_files(self) -> Dict[str, List[str]]:
        """读取所有词汇文件"""
        logger.info("开始读取词汇文件...")
        file_contents = {}
        
        if not os.path.exists(self.vocabulary_dir):
            logger.error(f"词汇目录 {self.vocabulary_dir} 不存在")
            return {}
            
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
                        cleaned_words = []
                        for word in words:
                            word = word.strip()
                            if word and not word.startswith('#') and len(word) > 0:
                                cleaned_words.append(word)
                        
                        file_contents[filename] = cleaned_words
                        logger.info(f"读取文件 {filename}: {len(cleaned_words)} 个词汇")
                        
                except Exception as e:
                    logger.error(f"读取文件 {filename} 失败: {e}")
                    
        return file_contents

    def classify_word(self, word: str) -> str:
        """对单个词汇进行分类"""
        word_lower = word.lower()
        
        # 检查政治类
        for pattern in self.political_patterns:
            if re.search(pattern, word, re.IGNORECASE):
                return 'political'
        
        # 检查色情类  
        for pattern in self.pornographic_patterns:
            if re.search(pattern, word, re.IGNORECASE):
                return 'pornographic'
        
        # 检查暴力类
        for pattern in self.violent_patterns:
            if re.search(pattern, word, re.IGNORECASE):
                return 'violent'
        
        # 检查赌博类
        for pattern in self.gambling_patterns:
            if re.search(pattern, word, re.IGNORECASE):
                return 'gambling'
        
        # 检查广告类
        for pattern in self.advertising_patterns:
            if re.search(pattern, word, re.IGNORECASE):
                return 'advertising'
        
        # 默认归类为其他
        return 'others'

    def classify_by_filename(self, filename: str) -> str:
        """根据文件名推断主要类别"""
        filename_lower = filename.lower()
        
        if '色情' in filename or 'porn' in filename_lower:
            return 'pornographic'
        elif '暴恐' in filename or '暴力' in filename or 'violent' in filename_lower:
            return 'violent'  
        elif '反动' in filename or '政治' in filename or 'political' in filename_lower:
            return 'political'
        elif '贪腐' in filename or '民生' in filename:
            return 'political'  # 贪腐和民生通常涉及政治
        elif '赌' in filename or 'gambling' in filename_lower:
            return 'gambling'
        elif '广告' in filename or 'ad' in filename_lower:
            return 'advertising'
        else:
            return 'others'

    def process_and_classify(self) -> Tuple[Dict[str, Set[str]], Dict[str, int]]:
        """处理和分类所有词汇"""
        logger.info("开始处理和分类词汇...")
        
        file_contents = self.read_vocabulary_files()
        if not file_contents:
            logger.error("没有读取到任何词汇文件")
            return {}, {}
        
        # 统计信息
        total_words_before = 0
        file_word_counts = {}
        
        # 收集所有词汇和其分类，避免重复
        word_classifications = {}  # word -> category
        
        for filename, words in file_contents.items():
            total_words_before += len(words)
            file_word_counts[filename] = len(words)
            
            # 根据文件名推断主要类别
            main_category = self.classify_by_filename(filename)
            
            logger.info(f"处理文件 {filename} (推断类别: {main_category})")
            
            for word in words:
                word = word.strip()
                if len(word) == 0:
                    continue
                
                # 如果词汇已经分类过，使用优先级判断
                if word in word_classifications:
                    existing_category = word_classifications[word]
                    
                    # 如果文件名明确指向某个类别，优先使用该类别
                    if main_category in ['pornographic', 'violent', 'political'] and main_category != 'others':
                        new_category = main_category
                    else:
                        # 否则使用智能分类
                        new_category = self.classify_word(word)
                    
                    # 优先级: political > pornographic > violent > gambling > advertising > others
                    priority = {
                        'political': 6,
                        'pornographic': 5, 
                        'violent': 4,
                        'gambling': 3,
                        'advertising': 2,
                        'others': 1
                    }
                    
                    if priority.get(new_category, 0) > priority.get(existing_category, 0):
                        word_classifications[word] = new_category
                else:
                    # 首次分类
                    if main_category in ['pornographic', 'violent', 'political'] and main_category != 'others':
                        category = main_category
                    else:
                        # 否则使用智能分类
                        category = self.classify_word(word)
                    
                    word_classifications[word] = category
        
        # 按类别组织词汇
        classified_words = defaultdict(set)
        for word, category in word_classifications.items():
            classified_words[category].add(word)
        
        # 统计去重后的词汇数量
        total_words_after = sum(len(words) for words in classified_words.values())
        
        statistics = {
            'total_before': total_words_before,
            'total_after': total_words_after,
            'duplicates_removed': total_words_before - total_words_after,
            'file_counts': file_word_counts,
            'category_counts': {cat: len(words) for cat, words in classified_words.items()}
        }
        
        logger.info(f"处理完成: 总词汇 {total_words_before} -> {total_words_after}, 去重 {statistics['duplicates_removed']} 个")
        
        return dict(classified_words), statistics

    def create_output_structure(self, classified_words: Dict[str, Set[str]], statistics: Dict[str, int]):
        """创建输出文件结构"""
        logger.info("创建输出文件结构...")
        
        # 创建输出目录
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            logger.info(f"创建目录: {self.output_dir}")
        
        # 生成分类文件
        for category, words in classified_words.items():
            if not words:
                continue
                
            filename = f"{category}.txt"
            filepath = os.path.join(self.output_dir, filename)
            
            # 按字母顺序排序
            sorted_words = sorted(list(words))
            
            with open(filepath, 'w', encoding='utf-8') as f:
                for word in sorted_words:
                    f.write(word + '\n')
            
            logger.info(f"生成文件: {filename} ({len(sorted_words)} 个词汇)")
        
        # 生成README文档
        self.create_readme(statistics)
        
        # 生成统计文件
        self.create_statistics_file(statistics)

    def create_readme(self, statistics: Dict[str, int]):
        """创建README文档"""
        readme_content = f"""# 敏感词库分类结果

## 概述

本目录包含经过分类整理的敏感词库，所有词汇均已去重并按类别分类。

## 文件说明

### 分类文件
"""

        for category, chinese_name in self.categories.items():
            count = statistics['category_counts'].get(category, 0)
            if count > 0:
                readme_content += f"- **{category}.txt** - {chinese_name} ({count:,} 个词汇)\n"

        readme_content += f"""
### 其他文件
- **README.md** - 本说明文档
- **statistics.txt** - 详细统计信息

## 统计摘要

- **处理前总词汇数**: {statistics['total_before']:,}
- **处理后总词汇数**: {statistics['total_after']:,}  
- **去除重复词汇**: {statistics['duplicates_removed']:,}
- **去重率**: {(statistics['duplicates_removed'] / statistics['total_before'] * 100):.1f}%

## 分类说明

- **政治类 (political.txt)**: 包含政治敏感词汇，如政治人物、政治事件、政治概念等
- **色情类 (pornographic.txt)**: 包含色情相关词汇
- **暴力类 (violent.txt)**: 包含暴力、恐怖主义相关词汇
- **赌博类 (gambling.txt)**: 包含赌博相关词汇
- **广告类 (advertising.txt)**: 包含广告、营销、诈骗相关词汇
- **其他类 (others.txt)**: 包含其他敏感词汇

## 使用说明

1. 根据需要选择相应的分类文件
2. 建议结合具体应用场景调整词汇列表
3. 定期更新以保持词汇库的时效性

## 生成时间

{datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}

---

*此分类结果由自动化脚本生成，如有问题请及时反馈。*
"""

        readme_path = os.path.join(self.output_dir, 'README.md')
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        logger.info("生成README.md文档")

    def create_statistics_file(self, statistics: Dict[str, int]):
        """创建统计文件"""
        stats_content = f"""敏感词库处理统计报告
======================

生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 总体统计

处理前总词汇数: {statistics['total_before']:,}
处理后总词汇数: {statistics['total_after']:,}
去除重复词汇: {statistics['duplicates_removed']:,}
去重率: {(statistics['duplicates_removed'] / statistics['total_before'] * 100):.2f}%

## 原始文件统计

"""
        
        for filename, count in statistics['file_counts'].items():
            stats_content += f"{filename}: {count:,} 个词汇\n"

        stats_content += "\n## 分类结果统计\n\n"
        
        for category, chinese_name in self.categories.items():
            count = statistics['category_counts'].get(category, 0)
            percentage = (count / statistics['total_after'] * 100) if statistics['total_after'] > 0 else 0
            stats_content += f"{chinese_name} ({category}.txt): {count:,} 个词汇 ({percentage:.1f}%)\n"

        stats_content += f"\n## 处理日志\n\n处理完成于: {datetime.now().isoformat()}\n"

        stats_path = os.path.join(self.output_dir, 'statistics.txt')
        with open(stats_path, 'w', encoding='utf-8') as f:
            f.write(stats_content)
        
        logger.info("生成statistics.txt统计文件")

    def run(self):
        """运行完整的分类流程"""
        logger.info("开始敏感词库分类任务...")
        start_time = datetime.now()
        
        try:
            # 处理和分类
            classified_words, statistics = self.process_and_classify()
            
            if not classified_words:
                logger.error("分类失败，没有处理到任何词汇")
                return False
            
            # 创建输出文件
            self.create_output_structure(classified_words, statistics)
            
            end_time = datetime.now()
            duration = end_time - start_time
            
            logger.info(f"任务完成! 耗时: {duration}")
            logger.info(f"输出目录: {self.output_dir}")
            
            return True
            
        except Exception as e:
            logger.error(f"任务执行失败: {e}", exc_info=True)
            return False


def main():
    """主函数"""
    classifier = SensitiveWordClassifier()
    success = classifier.run()
    
    if success:
        print("✅ 敏感词库分类任务完成!")
        print(f"📁 结果已保存到: {classifier.output_dir}")
    else:
        print("❌ 任务执行失败，请查看日志了解详情")
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())