# 敏感词库合并和JSON转换工具

## 功能说明

本工具用于将 `Vocabulary` 目录下的所有敏感词库文件合并成单一文件，并转换为JSON格式，方便在各种应用中使用。

## 使用方法

### 直接运行
```bash
python3 merge_to_json.py
```

### 在GitHub Actions中运行
脚本可以直接在GitHub Actions workflow中运行：
```yaml
- name: 生成合并的敏感词库JSON
  run: python3 merge_to_json.py
```

## 输出文件

运行后会生成两个文件：

1. **merged_sensitive_words.txt** - 合并的敏感词文本文件
   - 包含所有词汇的去重合并结果
   - 按字母顺序排序
   - 包含文件头注释信息

2. **merged_sensitive_words.json** - JSON格式的敏感词库
   - 符合要求的JSON结构
   - 包含元数据信息
   - 支持中文字符

## JSON文件格式

```json
{
  "metadata": {
    "source_file": "merged_sensitive_words.txt",
    "converted_time": "2025-08-11T06:55:19",
    "total_words": 43130,
    "description": "敏感词库 - 所有词汇的简单列表"
  },
  "words": [
    "词汇1",
    "词汇2",
    "..."
  ]
}
```

## 功能特性

- ✅ 自动读取 `Vocabulary` 目录下的所有 .txt 文件
- ✅ 智能去重，避免重复词汇
- ✅ 跳过注释行（以 # 开头）和空行
- ✅ 正确处理UTF-8编码和中文字符
- ✅ 生成符合规范的JSON格式
- ✅ 包含详细的元数据信息
- ✅ 提供完整的日志记录
- ✅ 自动验证生成的JSON文件格式

## 测试

运行测试脚本验证功能：
```bash
python3 test_merge_to_json.py
```

## 依赖要求

- Python 3.6+
- 标准库（无需额外安装包）

## 注意事项

- 脚本会覆盖已存在的 `merged_sensitive_words.txt` 和 `merged_sensitive_words.json` 文件
- 确保 `Vocabulary` 目录存在且包含 .txt 文件
- 生成的日志文件 `merge_to_json.log` 包含详细的处理信息