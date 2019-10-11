import re
from textblob import TextBlob
from textblob import Word
from collections import defaultdict
import math
def token_stream(line):

    li=TextBlob(line).words.singularize()
    li = ' '.join(li)  # 字符串
    terms = re.findall(r'\w+',li, re.I)
    result = []
    for word in terms:
        expected_str = Word(word)
        expected_str = expected_str.lemmatize("v")  # 将动词还原
        result.append(expected_str)
    return  result

# 匹配
def mapper(lineNum, list):
    # dic key为 lineNum:term value为 词频
    dic = {}
    for item in list:
        key = ''.join([str(lineNum), ':', item])
        if key in dic.keys():
            ll = dic.get(key)
            ll.append(1)
            dic[key] = ll
        else:
            dic[key] = [1]

    return dic
#将每个 term对应的 posting进行合并
def reducer(dic):
    keys = dic.keys()
    rdic = {}
    for key in keys:
        lineNum, kk = key.split(":")
        ss = ''.join([lineNum, ':', str(dic.get(key))]) #变成字符串
        if kk in rdic.keys():
            ll = rdic[kk]
            ll.append(ss)
            rdic[kk] = ll
        else:
            rdic[kk] = [ss]

    return rdic
# 结合 词频,得到每篇文章的词频
def combiner(dic):
    keys = dic.keys()
    tdic = {}
    for key in keys:
       # print(key)
        valuelist = dic.get(key) #得到记录 posting list
        count = 0
        for i in valuelist:
            count += i
        tdic[key] = count
    return tdic
#得到 文档id对应单词和词频
def doctoword(dic):
    tdic = {}
    for u in dic.keys():
        tweetid,word=u.split(':')
        tf=dic[u]
        if tweetid in tdic.keys():
            # ll=tdic[tweetid]
            # ll.append(''.join([word, ':', str(tf)]))
            # tdic[tweetid]=ll
            tdic[tweetid].append(''.join([word, ':', str(tf)]))
        else:
            tdic[tweetid]=[''.join([word, ':', str(tf)])]
    return tdic


#排序，返回一个列表
def shuffle(dic):
    dict = sorted(dic.items(), key=lambda x: x[0])
    return dict

# 去掉词频
def process(dic):
    pdic={}
    for word in dic.keys():
        lis=dic[word]
        for u in lis:
            x,y=u.split(':')
            if word in pdic.keys():
                ll=pdic[word]
                ll.append(x)
                pdic[word] = ll
            else:
                pdic[word] =[x]
    return pdic
# 输入包含（词——id和词频），得到 词频和 文档频率
def tfAnddf(dic):
    pdic=defaultdict(dict)
    for word in dic.keys():
        lis=dic[word]
        tf=0
        df=0
        for u in lis:
            x,y=u.split(':')
            tf=tf+int(y)  #统计词频
            df=df+1       #统计文档频率
        pdic[word]=[str(tf),str(df)]
    return pdic
# 处理 query建立 词与词频的字典
def procee_query(query):
    dic={}
    word=query.split()
    for u in word:
        if u in dic.keys():
            dic[u]=dic[u]+1
        else:
            dic[u]=1
    return dic

def documentTF(query,dic,postings):
    Answer={}
    for word in query.keys():
        if word in dic:
            for u in dic[word]:  #找到对应的文档id
                
                if tweetid in Answer.keys():
                    # ll=Answer[word]
                    # ll.append(str(df))
                    Answer[tweetid].append(df)
                else:
                    Answer[tweetid]=[df]
    return Answer



# def do_RankSearch(query,doc,postings):
#     answer={}
#     Sum=0
#     tfq={}
#     tfd={}
#     idf={}
#     for word in query.keys():
#         if word in doc.keys():
#             tfq[word] = 1 + math.log(query[word])
#             idf[word] = math.log(30548 / doc[word][1])
#             for u in postings[word]:
#                 tweetid, df = u.split(':')
#                 if tweetid in tfd.keys():
#                     tfd[tweetid] += df
#                 else:
#                     tfd[tweetid] = df
#     for word in query.keys():
#
#         tfd[word]=1+math.log(dic[word][0])  #在某一篇的文档
#
#
#     for u in tfd:
#         Sum=Sum+u**2
#     Sum=math.sqrt(Sum)
#
#     for word in query.keys():
#         answer[word]=

def get_reverse_index(filepath):
    file = open(filepath, 'r')
    rdic_p = {}
    for content in file.readlines():
        d = eval(content) #变成字典
        word = d['text']
        lineNum=d['tweetId']
        word=word.lower()
        if word == '':
            break
        list = token_stream(word)
        mdic = mapper(lineNum, list)
        #print(mdic)
        cdic = combiner(mdic)
        #print(cdic)
        rdic_p.update(cdic) #把cdic的键值赋值给 rdic_p

    rdic = reducer(rdic_p)

    sdic = shuffle(rdic)
    return rdic_p,dict(sdic)

def do_rankSearch(terms,postings):
    Answer = defaultdict(dict)
    for item in terms:
        if item in postings:
            for tweetid in postings[item]:
                if tweetid in Answer:
                    Answer[tweetid]+=1
                else:
                    Answer[tweetid] = 1
    Answer = sorted(Answer.items(),key = lambda asd:asd[1],reverse=True)
    return Answer


if __name__ == '__main__':
    filepath="F:\\信息检索\\tweets.txt"
    rdic,sdic= get_reverse_index(filepath)
    dic=doctoword(rdic)
    print(dic)
    # search_word = ' '
    # while(search_word!='q'):
    #     search_word = input('Please input the word you want to search (all lower):  ')
    #     dic=procee_query(search_word)
    #     doc = documentTF(dic, rdic)
    #     print(doc)
    # search_word=' '
    # while(search_word!='q'):
    #     answer_set = set()
    #     search_word = input('Please input the word you want to search (all lower):  ')
    #     search_word=search_word.lower()
    #     word_list=search_word.split()
    #     for i, word in enumerate(word_list):
    #         if word in dic.keys() and i == 0:
    #             answer_set = set(dic[word])
    #         elif i % 2 == 1 and i != len(word_list) - 1:
    #             if word == 'and':
    #                 if word_list[i + 1] in dic.keys():
    #                     x = set(dic[word_list[i + 1]])
    #                     answer_set.intersection_update(x)
    #             if word == 'or':
    #                 if word_list[i + 1] in dic.keys():
    #                     x = set(dic[word_list[i + 1]])
    #                     answer_set = answer_set.union(x)
    #
    #             if word == 'not':
    #                 if word_list[i + 1] in dic.keys():
    #                     x = set(dic[word_list[i + 1]])
    #                     answer_set.difference_update(x)
    #     print(answer_set)
    #
    #     leng = len(word_list)
    #     answer = do_rankSearch(word_list,dic)
    #     print("[Rank_Score: Tweetid]")
    #     for (tweetid, score) in answer:
    #         print(str(score / leng) + ": " + tweetid)

