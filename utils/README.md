# utils 工具部分函数说明

## split_word_meaning(meaning)

### 所属文件
utils/split_meaning.py

### 功能
拆分单词释义字符串，提取词性和对应翻译。

### 输入规则
- 词性和中文翻译用**一个空格**隔开；
- 单种词性内，同一种意思的不同描述用**英文逗号**隔开；
- 单种词性内，不同意思用**英文分号**隔开；
- 多种词性之间用**两个空格**隔开；
- 标准词性识别规则：**长度≤6**且以**英文句点**结尾（如 n.）。

### 所有标准词性参考
| 词性     | 含义    |
|--------|-------|
| n.     | 名词    |
| v.     | 动词    |
| vi.    | 不及物动词 |
| vt.    | 及物动词  |
| adj.   | 形容词   |
| adv.   | 副词    |
| prep.  | 介词    |
| conj.  | 连词    |
| pron.  | 代词    |
| num.   | 数词    |
| art.   | 冠词    |
| int.   | 感叹词   |
| aux.   | 助动词   |
| modal. | 情态动词  |

### 输入示例
```python
meaning = "n. 著作家,作者;创始人  v. 写作"
split_word_meaning(meaning)
```

### 输出示例
```python
[
    {"pos": "n.", "trans_list": ["著作家,作者", "创始人"]},
    {"pos": "v.", "trans_list": ["写作"]}
]
```

## split_word_example(example, example_trans)

### 所属文件
utils/split_example.py

### 功能
拆分单词例句和对应翻译字符串，保证例句与翻译列表长度一一对应。

### 输入规则
- 多个例句/翻译之间用**英文分号**隔开；
- 例句中的“**”为单词在例句中出现的位置，无需处理；
- 例句/翻译为空时，返回空列表。

### 输入示例
```python
example = "Our guest...**author**.;Another sentence."
example_trans = "我们今天的...作者。;另一个句子。"
split_word_example(example, example_trans)
```

### 输出示例
```python
{
    "example_list": ["Our guest...**author**.", "Another sentence."],
    "example_trans_list": ["我们今天的...作者。", "另一个句子。"]
}
```