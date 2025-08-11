# JSON文件压缩工具 / JSON File Compression Tools

该工具集用于优化`merged_sensitive_words.json`文件的大小，通过多种压缩方式显著减小文件体积，同时保持数据完整性。

## 功能特性

- ✅ **格式压缩**: 移除JSON中的空白字符和缩进
- ✅ **GZIP压缩**: 提供高效的二进制压缩
- ✅ **数据完整性验证**: 确保压缩前后数据一致
- ✅ **详细统计报告**: 提供压缩比例和空间节省信息
- ✅ **错误处理**: 完善的异常处理和日志记录

## 文件说明

### 核心脚本

1. **`generate_merged_json.py`** - 生成合并的敏感词JSON文件
2. **`compress_json.py`** - JSON文件压缩脚本

### 生成的文件

- `merged_sensitive_words.json` - 原始合并文件（带格式）
- `merged_sensitive_words_compressed.json` - 压缩格式的JSON文件
- `merged_sensitive_words_compressed.json.gz` - GZIP压缩版本
- `compression_report.json` - 压缩统计报告

## 使用方法

### 1. 生成合并的JSON文件

首先需要运行词汇分类脚本，然后生成合并文件：

```bash
# 1. 生成分类词汇（如果尚未运行）
python3 classify_vocabulary.py

# 2. 生成合并的JSON文件
python3 generate_merged_json.py
```

### 2. 压缩JSON文件

```bash
# 压缩默认文件（merged_sensitive_words.json）
python3 compress_json.py

# 压缩指定文件
python3 compress_json.py your_file.json
```

## 压缩效果

基于当前敏感词库（43,130个词汇）的压缩效果：

| 版本 | 文件大小 | 压缩比例 | 空间节省 |
|------|----------|----------|----------|
| 原始文件 | 980.9 KB | - | - |
| JSON压缩 | 770.2 KB | 21.5% | 210.7 KB |
| GZIP压缩 | 294.3 KB | 70.0% | 686.6 KB |

## 文件结构

### 原始JSON结构

```json
{
  "lastUpdateDate": "2025/08/11",
  "totalCount": 43130,
  "description": "合并后的敏感词库...",
  "categories": {
    "political": "政治类",
    "pornographic": "色情类",
    ...
  },
  "words": ["词汇1", "词汇2", ...]
}
```

### 压缩原理

1. **JSON格式压缩**:
   - 移除所有缩进和换行符
   - 去除JSON键值对之间的空格
   - 使用紧凑的分隔符 `,` 和 `:`

2. **GZIP压缩**:
   - 在JSON格式压缩基础上应用GZIP算法
   - 利用重复模式实现更高压缩比
   - 适合网络传输和长期存储

## 数据完整性保证

压缩工具包含以下验证机制：

- ✅ **词汇数量验证**: 确保`totalCount`与实际词汇数一致
- ✅ **内容一致性检查**: 逐一比较原始和压缩后的词汇
- ✅ **JSON格式验证**: 确保压缩后仍为有效JSON
- ✅ **元数据保留**: 保持所有重要的元数据字段

## 性能优化建议

### 推荐用途

1. **开发环境**: 使用原始格式文件，便于阅读和调试
2. **生产环境**: 使用JSON压缩版本，减少内存占用
3. **存储/传输**: 使用GZIP版本，最大化空间和带宽节省

### 集成建议

```python
# 在Python中加载压缩的JSON文件
import json
import gzip

# 方法1：加载JSON压缩版本
with open('merged_sensitive_words_compressed.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 方法2：加载GZIP版本
with gzip.open('merged_sensitive_words_compressed.json.gz', 'rt', encoding='utf-8') as f:
    data = json.load(f)
```

## 脚本参数

### generate_merged_json.py

- 自动从`classified_vocabulary`目录读取分类文件
- 输出到`merged_sensitive_words.json`

### compress_json.py

```bash
# 基本用法
python3 compress_json.py [input_file]

# 示例
python3 compress_json.py custom_file.json
```

## 错误处理

脚本包含完善的错误处理机制：

- 文件不存在检查
- JSON格式验证
- 编码错误处理
- 磁盘空间检查
- 权限验证

## 日志记录

所有操作都有详细的日志记录：

- 信息级别: 正常操作进度
- 警告级别: 非致命问题
- 错误级别: 导致失败的问题

## 技术要求

- Python 3.6+
- 标准库模块: `json`, `gzip`, `logging`, `datetime`
- 内存要求: 约50MB（用于处理43K词汇）

## 维护说明

1. **定期更新**: 当敏感词库更新时，重新运行压缩流程
2. **版本控制**: 建议只提交压缩版本到版本控制系统
3. **备份策略**: 保留原始文件作为备份

## 许可证

本工具集遵循项目的开源许可证，可自由使用和修改。