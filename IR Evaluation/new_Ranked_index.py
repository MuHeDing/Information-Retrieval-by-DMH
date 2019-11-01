import re
from textblob import TextBlob
from textblob import Word
from collections import defaultdict
from math import *

length = {}
test={}
def token_stream(line):
    #先变小写，然后名词变成单数
    line=line.lower()
    li=TextBlob(line).words.singularize()
    li = ' '.join(li)  # 列表变成 字符串
    terms = re.findall(r'\w+',li, re.I) # 只匹配字符和数字
    result = []
    for word in terms:
        expected_str = Word(word)
        expected_str = expected_str.lemmatize("v")  # 将动词还原
        result.append(expected_str)
    return  result

# 得到文章向量
def dfvector(tweetid, list):
    # 得到 文章向量的长度
    dic={}
    for u in list:
        if u in dic.keys():
            dic[u]=dic[u]+1
        else:
            dic[u]=1
    sum=0
    for a in dic.values():
        u=1+log(a,10)
        sum=sum+pow(u,2)

    sum=sqrt(sum)
    length[tweetid]=sum



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
    for term in  rdic.keys():  # 对postings进行排序
        rdic[term].sort()
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
    #print(pdic)
    return pdic
# 处理 query建立 词与词频的字典
def process_query(query):
    dic={}
    word=token_stream(query.lower())
    #print(word)
    for u in word:
        if u in dic.keys():
            dic[u]=dic[u]+1
        else:
            dic[u]=1
    return dic


def do_RankSearch(query,doc,tdic):
    score={}
    for term in query.keys():
        ll=query[term]
        ll=1+log(ll,10)  # query中的词频
        #print('ll: ',ll)
        if term in tdic.keys():  # 乘以 idf
           df=int(tdic[term][1])
         #  print('df: ',df)
           idf=log(30548/df,10)
           ll=ll*idf
         #  print('ll2: ',ll)
        if term in doc.keys():
            for postings in doc[term]:
                tweetid,tf=postings.split(':')
                tf=int(tf)
                tf = 1 + log(tf,10)
               # print('tf: ',tf)
                if tweetid  in score.keys():
                    score[tweetid]=score[tweetid]+ll*tf
                else:
                    score[tweetid]=ll*tf
    for tweetid in score.keys():
       score[tweetid]=score[tweetid]/length[tweetid]


    return score



def get_reverse_index(filepath):
    file = open(filepath, 'r')
    rdic_p = {}
    i=0
    for content in file.readlines():
        d = eval(content) #变成字典
        word = d['text']
        lineNum=d['tweetId']
        if word == '':
            break
        test[lineNum] = word
        list = token_stream(word)
        dfvector(lineNum, list)
        mdic = mapper(lineNum, list)
        #print(mdic)
        cdic = combiner(mdic)
        #print(cdic)
        rdic_p.update(cdic) #把cdic的键值赋值给 rdic_p

    rdic = reducer(rdic_p)

    sdic = shuffle(rdic)
    return dict(sdic) # 第一个参数为还没合并的

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
def old_do_rankSearch(terms,postings):
    Answer = defaultdict(dict)
    for item in terms:
        if item in postings:
            for tweetid in postings[item]:
                if tweetid in Answer:
                    Answer[tweetid]+=1
                else:
                    Answer[tweetid] = 1
    Answer = sorted(Answer.items(),key = lambda asd:asd[1],reverse=True)
    #print("[Rank_Score: Tweetid]")
    return dict(Answer)

if __name__ == '__main__':

    #  you are a good boy but Bachmann To Give Her Own State Of you Environmental groups in China are criticizing come on boy
    k = 100
    filepath="F:\\信息检索\\tweets.txt"
    dic= get_reverse_index(filepath)
    tf_dic = tfAnddf(dic)

    # search_word = input('Please input the word you want to search (all lower):  ')
    # query = process_query(search_word)
    # score = do_RankSearch(query, dic, tf_dic)
    # score=dict(sorted(score.items(), key=lambda x: x[1],reverse=True))
    # answer = {}
    # for i, key in enumerate(score.keys()):
    #     text=test[key]
    #     print(text)
    #     if i ==k:
    #         break
   # search_word = ' '

    # while(1):
    #     query=input('Please input the word you want to search (all lower):  ')
    #     query = process_query(query)
    #     x = process(dic)
    #     score=old_do_rankSearch(query,x)
    #     #score = dict(sorted(score.items(), key=lambda x: x[1], reverse=True))
    #     for i, key in enumerate(score.keys()):
    #         text=test[key]
    #         print(text)
    #         if i ==k:
    #             break

    #读取query文件，返回结果
    with open('F:\\信息检索\\try\\final_result.txt', 'w', encoding='utf-8') as f_out:
        with open('F:\\信息检索\\evaluation\\MB171-225.txt', 'r', encoding='utf-8') as file:
            lis = []
            for line in file.readlines():
                if line.find('<query>') != -1:
                    line = re.sub('<query>|</query>', '', line)
                    line = line.strip()
                    lis.append(line)
        id=171
        for query in lis:
            query = process_query(query)
            score=do_RankSearch(query,dic,tf_dic)
            score = dict(sorted(score.items(), key=lambda x: x[1], reverse=True))
            for i, key in enumerate(score.keys()):
                text=str(id)+' '+key
                f_out.write(text+'\n')
                if i ==k:
                    break
            id=id+1

    # while(1):
    #     search_word = input('Please input the word you want to search (all lower):  ')
    #     query=process_query(search_word)
    #
    #     score = do_RankSearch(query, dic,tf_dic)
    #     score=dict(sorted(score.items(), key=lambda x: x[1],reverse=True))
    #     answer = {}
    #     for i,(key, value) in enumerate(score.items()):
    #         print(key,' : ',value)
    #         answer[key] = value
    #         if i == k:
    #             break
