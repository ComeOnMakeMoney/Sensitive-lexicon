#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
敏感词库合并脚本
将 Vocabulary 目录中的分类敏感词文件合并为单一文件
"""

import os
import datetime
import locale
from collections import defaultdict
from typing import Dict, Set, List

# 尝试设置中文排序
try:
    locale.setlocale(locale.LC_ALL, 'zh_CN.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_ALL, 'C.UTF-8')
    except:
        pass


def read_vocabulary_file(file_path: str) -> Set[str]:
    """
    读取词汇文件，返回去重后的词汇集合
    
    Args:
        file_path: 文件路径
        
    Returns:
        去重后的词汇集合
    """
    words = set()
    try:
        # 尝试不同的编码
        for encoding in ['utf-8', 'gbk', 'gb2312']:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    content = f.read().strip()
                    
                    # 检查内容是否为逗号分隔的格式
                    if ',' in content and content.count(',') > content.count('\n'):
                        # 逗号分隔格式
                        for word in content.split(','):
                            word = word.strip()
                            if word and not word.startswith('#'):
                                words.add(word)
                    else:
                        # 换行分隔格式
                        for line in content.split('\n'):
                            word = line.strip()
                            if word and not word.startswith('#'):
                                words.add(word)
                    
                    break
            except UnicodeDecodeError:
                continue
                
    except Exception as e:
        print(f"警告：读取文件 {file_path} 时出错: {e}")
    
    return words


def is_gambling_word(word: str) -> bool:
    """
    判断是否为赌博相关词汇
    
    Args:
        word: 待判断的词汇
        
    Returns:
        是否为赌博相关词汇
    """
    gambling_keywords = [
        "赌", "博", "彩", "押", "注", "筹码", "轮盘", "老虎机", "百家乐", "21点", 
        "德州", "梭哈", "麻将", "骰子", "赌场", "赌桌", "赌神", "赌王", "赌徒",
        "赌博", "博彩", "投注", "下注", "打牌", "牌局", "庄家", "庄闲", "大小",
        "单双", "开奖", "中奖", "特码", "特肖", "六合", "福彩", "体彩", "彩票",
        "彩金", "赛马", "竞猜", "竞彩", "足彩", "球彩", "连线", "转盘", "骰宝"
    ]
    
    return any(keyword in word for keyword in gambling_keywords)


def get_category_mapping() -> Dict[str, List[str]]:
    """
    定义文件到类别的映射关系
    
    Returns:
        类别映射字典
    """
    return {
        "基础违法词汇": ["反动词库.txt", "贪腐词库.txt"],
        "暴力相关": ["暴恐词库.txt"],
        "色情相关": ["色情词库.txt"],
        "赌博相关": [],  # 将从其他文件中提取赌博相关词汇
        "政治敏感": ["反动词库.txt", "GFW补充词库.txt"],
        "广告营销": ["民生词库.txt"],
        "其他敏感词汇": ["其他词库.txt", "补充词库.txt", "COVID-19词库.txt", "零时-Tencent.txt"]
    }


def merge_vocabulary_files(vocabulary_dir: str) -> Dict[str, Set[str]]:
    """
    合并词汇文件到不同类别
    
    Args:
        vocabulary_dir: 词汇文件目录
        
    Returns:
        按类别分组的词汇字典
    """
    category_mapping = get_category_mapping()
    merged_categories = defaultdict(set)
    all_words = set()  # 用于收集所有词汇以便提取赌博词汇
    
    # 获取目录中的所有txt文件
    if not os.path.exists(vocabulary_dir):
        print(f"错误：目录 {vocabulary_dir} 不存在")
        return {}
    
    # 首先读取所有词汇
    all_files = [f for f in os.listdir(vocabulary_dir) if f.endswith('.txt')]
    
    for filename in all_files:
        file_path = os.path.join(vocabulary_dir, filename)
        words = read_vocabulary_file(file_path)
        all_words.update(words)
    
    # 提取赌博相关词汇
    gambling_words = {word for word in all_words if is_gambling_word(word)}
    merged_categories["赌博相关"] = gambling_words
    
    # 按照映射关系分类其他词汇
    for category, files in category_mapping.items():
        if category == "赌博相关":  # 跳过，已经处理过了
            continue
            
        for filename in files:
            file_path = os.path.join(vocabulary_dir, filename)
            if os.path.exists(file_path):
                words = read_vocabulary_file(file_path)
                # 从其他类别中移除已归类为赌博的词汇
                words = words - gambling_words
                merged_categories[category].update(words)
                print(f"已处理文件: {filename} -> {category} ({len(words)} 个词汇)")
            else:
                print(f"警告：文件 {filename} 不存在")
    
    print(f"已提取赌博相关词汇: {len(gambling_words)} 个")
    
    return dict(merged_categories)


def generate_file_header(categories: Dict[str, Set[str]]) -> str:
    """
    生成文件头部信息
    
    Args:
        categories: 分类词汇字典
        
    Returns:
        文件头部字符串
    """
    total_words = sum(len(words) for words in categories.values())
    total_categories = len(categories)
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    header = f"""# 敏感词库合并文件
# 生成时间: {current_time}
# 总词汇数: {total_words}
# 分类数: {total_categories}
# 
# 使用说明：
# - 每个类别以#号开头
# - 词汇按字母顺序排列
# - 已去除重复词汇
# 
# ==========================================

"""
    return header


def write_merged_file(categories: Dict[str, Set[str]], output_path: str):
    """
    写入合并后的文件
    
    Args:
        categories: 分类词汇字典
        output_path: 输出文件路径
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            # 写入文件头部
            header = generate_file_header(categories)
            f.write(header)
            
            # 按类别写入词汇
            for category, words in categories.items():
                f.write(f"# {category}\n")
                
                # 按字母顺序排序
                sorted_words = sorted(words)
                for word in sorted_words:
                    f.write(f"{word}\n")
                
                f.write("\n")  # 类别之间用空行分隔
        
        print(f"合并完成！输出文件: {output_path}")
        
        # 输出统计信息
        total_words = sum(len(words) for words in categories.values())
        print(f"总词汇数: {total_words}")
        print(f"分类数: {len(categories)}")
        for category, words in categories.items():
            print(f"  {category}: {len(words)} 个词汇")
            
    except Exception as e:
        print(f"错误：写入文件时出错: {e}")


def main():
    """主函数"""
    # 设置路径
    script_dir = os.path.dirname(os.path.abspath(__file__))
    vocabulary_dir = os.path.join(script_dir, "Vocabulary")
    output_path = os.path.join(script_dir, "merged_sensitive_words.txt")
    
    print("开始合并敏感词库...")
    print(f"词汇目录: {vocabulary_dir}")
    print(f"输出文件: {output_path}")
    print("-" * 50)
    
    # 合并词汇文件
    categories = merge_vocabulary_files(vocabulary_dir)
    
    if not categories:
        print("错误：没有找到任何词汇文件")
        return
    
    # 写入合并后的文件
    write_merged_file(categories, output_path)


if __name__ == "__main__":
    main()