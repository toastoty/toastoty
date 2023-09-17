import os
import jieba
import gensim
import re
import cProfile

# 获取指定路径的文件内容
def get_file_contents(path):
    string = ''
    with open(path, 'r', encoding='UTF-8') as f:
        string = f.read()
    return string

# 将读取到的文件内容先把标点符号、转义符号等特殊符号过滤掉，然后再进行结巴分词
def filter(text):
    pattern = re.compile(u"[^a-zA-Z0-9\u4e00-\u9fa5]")
    text = pattern.sub("", text)
    result = jieba.lcut(text)
    return result

# 传入过滤之后的数据，通过调用gensim.similarities.Similarity计算余弦相似度
def calc_similarity(text1, text2):
    texts = [text1, text2]
    dictionary = gensim.corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    similarity = gensim.similarities.Similarity('-Similarity-index', corpus, num_features=len(dictionary))
    test_corpus_1 = dictionary.doc2bow(text1)
    cosine_sim = similarity[test_corpus_1][1]
    return cosine_sim

def main_test():
    path1 = input("输入论文原文的文件的绝对路径：")
    path2 = input("输入抄袭版论文的文件的绝对路径：")
    if not os.path.exists(path1):
        print("论文原文文件不存在！")
        exit()
    if not os.path.exists(path2):
        print("抄袭版论文文件不存在！")
        exit()
    str1 = get_file_contents(path1)
    str2 = get_file_contents(path2)
    text1 = filter(str1)
    text2 = filter(str2)
    similarity = calc_similarity(text1, text2)  # 生成的similarity变量类型为<class 'numpy.float32'>
    result = round(similarity.item(), 2)  # 借助similarity.item()转化为<class 'float'>，然后再取小数点后两位
    print("文章相似度： %.4f" % result)  # 修正此处的变量名
    return result

if __name__ == '__main__':
    profiler = cProfile.Profile()
    profiler.enable()
    similarity = main_test()
    save_path = "similarity.txt"  # 请设置保存相似度结果的文件路径
    # 将相似度结果写入指定文件
    with open(save_path, 'w', encoding="utf-8") as f:
        f.write("文章相似度： %.4f" % similarity)
    profiler.disable()
    profiler.print_stats(sort='cumulative')
