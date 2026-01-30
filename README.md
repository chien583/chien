# 论著草稿生成器

该仓库提供一个生成论著草稿的脚本，可用于形成《促进革命老区、民族地区、边疆地区等振兴发展的差异化政策研究》书稿的初始内容。脚本会依据 `outline.json` 的章节结构生成章节文件，并合并输出为一份总稿。

## 使用方式

```bash
python3 book_generator.py --output-dir dist --target-words 500000
```

## 输出内容

- `dist/manuscript.md`：完整书稿汇总
- `dist/chapter_XX.md`：按章节拆分的草稿文件
