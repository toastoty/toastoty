# 软工作业2：python实现简易论文查重
| 这个作业属于哪个课程 | [计科21级1 2班](https://edu.cnblogs.com/campus/gdgy/CSGrade21-12) |
| -------------------- | ------------------------------------------------------------ |
| 这个作业要求在哪里   | [个人项目](https://edu.cnblogs.com/campus/gdgy/CSGrade21-12/homework/13014) |
| 这个作业的目标       |                                                              |
项目Github[点击这里](https://github.com/toastoty/toastoty)
## PSP表

| PSP2.1                                  | Personal Software Process               | 预估耗时（分钟） | 实际耗时（分钟） |
| --------------------------------------- | --------------------------------------- | ---------------- | ---------------- |
| Planning                                | 计划                                    | 10               | 10               |
| · Estimate                              | · 估计这个任务需要多少时间              | 5                | 5                |
| Development                             | 开发                                    | 770              | 700              |
| · Analysis                              | · 需求分析 (包括学习新技术)             | 210              | 180              |
| · Design Spec                           | · 生成设计文档                          | 50               | 30               |
| · Design Review                         | · 设计复审                              | 10               | 10               |
| · Coding Standard                       | · 代码规范 (为目前的开发制定合适的规范) | 20               | 20               |
| · Design                                | · 具体设计                              | 30               | 20               |
| · Coding                                | · 具体编码                              | 180              | 180              |
| · Code Review                           | · 代码复审                              | 60               | 30               |
| · Test                                  | · 测试（自我测试，修改代码，提交修改）  | 90               | 120              |
| Reporting                               | 报告                                    | 60               | 60               |
| · Test Report                           | · 测试报告                              | 20               | 20               |
| · Size Measurement                      | · 计算工作量                            | 20               | 10               |
| · Postmortem & Process Improvement Plan | · 事后总结, 并提出过程改进计划          | 20               | 20               |
| · 合计                                  |                                         | 785              | 715              |
## 运行环境
PyCharm Community Edition 2022.3.2


## 计算模块接口的设计与实现过程
###  jieba.cut

用于对中文句子进行分词
代码：

```python
seg_list = jieba.cut("他来到了网易杭研大厦")
print("/ ".join(seg_list))
```

运行结果：

```
他/ 来到/ 了/ 网易/ 杭研/ 大厦
```


### re.compile

由于对比对象为中文或英文单词，因此应该对读取到的文件数据中存在的特殊符号（如换行符\n过滤掉）这里选择用正则表达式来匹配符合的数据。

代码：

```python
# 将读取到的文件内容先把标点符号、转义符号等特殊符号过滤掉，然后再进行结巴分词
def filter(string):
    pattern = re.compile(u"[^a-zA-Z0-9\u4e00-\u9fa5]")
    string = pattern.sub("", string)
    result = jieba.lcut(string)
    return result

```


## gensim.dictionary.doc2bow

`gensim.dictionary.doc2bow` 函数是 Gensim 库中用于将文档转换为词袋（Bag of Words）表示的功能之一。它用于构建文本数据的数值表示，通常用于文本挖掘、主题建模和信息检索等任务。以下是该函数的详细用法：

```python
doc2bow(document, allow_update=False, return_missing=False)
```

参数解释：
- `document`：要转换为词袋表示的文档，通常是一个已分词的文本，可以是字符串列表（每个元素代表一个文档）或字符串（单个文档）。
- `allow_update`（可选）：如果为 `True`，则会更新字典（词汇表）以包括文档中的新单词。默认为 `False`，不更新字典。
- `return_missing`（可选）：如果为 `True`，则会返回文档中不在字典中的单词的信息。默认为 `False`。

返回值：
- 返回一个词袋表示的文档，它是一个包含元组 `(word_id, word_count)` 的列表，其中 `word_id` 是单词在词汇表中的整数标识符，`word_count` 是单词在文档中的出现次数。

示例用法：

```python
from gensim import corpora

# 创建词汇表
dictionary = corpora.Dictionary([["apple", "banana", "cherry"], ["apple", "banana", "date"]])

# 文档
document = "apple apple banana"

# 将文档转换为词袋表示
bow = dictionary.doc2bow(document.split())

print(bow)
```

该向量bow与原来文本中单词出现的顺序没有关系，而是词典中每个单词在文本中出现的频率。


## gensim.similarities.Similarity

`gensim.similarities.Similarity` 是 Gensim 库中用于计算文档相似性的类。它基于一种称为“余弦相似度（Cosine Similarity）”的度量方法来衡量文档之间的相似性。

余弦相似度衡量两个向量的夹角余弦值，值越接近1，表示向量越相似，值越接近0，表示向量越不相似。在文档相似性计算中，每个文档被表示为一个向量，其中向量的每个维度对应一个词汇表中的单词，该维度的值表示单词在文档中的权重（通常使用词频或TF-IDF权重）。然后，通过计算两个文档向量的余弦相似度来度量它们之间的相似性。

`gensim.similarities.Similarity` 的工作原理如下：

1. **准备文档向量：** 首先，为每个文档创建一个向量表示。这可以是词袋向量（每个维度对应一个单词，值表示单词在文档中的出现次数），也可以是TF-IDF向量（每个维度对应一个单词，值表示单词的TF-IDF权重）等。

2. **构建索引：** 使用这些文档向量构建索引，以便快速计算相似性。索引的类型可以是LSI（Latent Semantic Indexing）、LDA（Latent Dirichlet Allocation）等。

3. **计算相似性：** 当需要计算文档之间的相似性时，将目标文档表示为向量，并使用索引来查找与目标文档最相似的文档。这通常涉及计算目标文档与索引中每个文档的余弦相似度，并根据相似度得分进行排序。

4. **返回结果：** 返回与目标文档最相似的文档，通常按照相似度得分排序。可以根据需要返回前N个最相似的文档。

   

## 计算模块接口部分的性能改进



406518 function calls (406500 primitive calls) in 31.625 seconds

   |ncalls | tottime|  percall | cumtime | percall| filename:lineno(function)|
   | --------|---------- | ---------- | ---------------- |-----------|--------------|
   |     1   | 0.000    |0.000   |31.624  | 31.624 |main.py:31(main_test)|
   |     2   |31.053  | 15.526   |31.053 |  15.526| {built-in method builtins.input}|
   |     2    |0.000  |  0.000 |   0.544  |  0.272 |main.py:15(filter)|
   |     2  |  0.001 |   0.000 |   0.542  |  0.271| __init__.py:356(lcut)|
   | 12125   | 0.002  |  0.000  |  0.541  |  0.000| __init__.py:289(cut)|
   | 12125  |  0.00  |  0.000 |   0.539 |   0.000| __init__.py:249(__cut_DAG)|

主要的性能瓶颈出现在 `jieba` 库的分词过程中，特别是在`__cut_DAG` 函数的调用上。下面是对性能瓶颈的分析和可能的改进方法：

1. **分词效率低下：** 性能分析结果表明 `jieba` 的分词操作占用了大部分的时间。这可能是因为文本中包含大量的词汇，导致分词成为计算密集型操作。

2. **频繁的函数调用：** 除了 `__cut_DAG`，`jieba` 的其他函数也被频繁调用，这可能增加了函数调用的开销。

3. **输入处理：** `input()` 函数也占用了一定的时间，因为它等待用户输入。在性能分析中，你可以看到 `input()` 函数被调用了两次，占用了大约 31 秒的时间。

基于这些观察，以下是一些可能的改进方法：

1. **优化分词过程：** 考虑优化分词过程。可能的优化包括使用更快速的分词库，或者对文本进行预处理以减少分词的工作量。

2. **减少函数调用：** 尽量减少频繁的函数调用，特别是在性能关键部分。可以将一些操作合并为更大的块，减少函数调用的开销。

3. **异步输入：**考虑使用异步输入方式，以便在等待输入时可以继续执行其他操作，而不是阻塞整个程序。

   

## 计算模块部分单元测试展示

新建单元测试文件unitTest.py：

```python
import unittest
from main import main_test


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(main_test(),0.99)   #首先假设预测的是前面第一组运行的测试数据


if __name__ == '__main__':
    unittest.main()

```

![image-20230917210736339](C:\Users\15147\AppData\Roaming\Typora\typora-user-images\image-20230917210736339.png)



## 计算模块部分异常处理说明

使用`os.path.exists()`检验文件是否存在：

```python

def main_test():
    path1 = input("输入论文原文的文件的绝对路径：")
    path2 = input("输入抄袭版论文的文件的绝对路径：")
    if not os.path.exists(path1) :
        print("论文原文文件不存在！")
        exit()
    if not os.path.exists(path2):
        print("抄袭版论文文件不存在！")
        exit()
    
```