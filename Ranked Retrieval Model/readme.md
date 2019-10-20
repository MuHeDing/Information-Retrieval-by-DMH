# Information Retrieval—Ranked retrieval model

## **实验内容**

### 1. 在Homework1.1的基础上实现最基本的Ranked retrieval model
1. • Input：a query (like Ron Weasley birthday)
2. • Output: Return the top K (e.g., K = 10) relevant tweets.
3. • Use SMART notation: lnc.ltc
4. • Document: logarithmic tf (l as first character), no idf and cosine
normalization
5. • Query: logarithmic tf (l in leftmost column), idf (t in second column), nonormalization

### 2. 改进Inverted index
1. • 在Dictionary中存储每个term的DF
2. • 在posting list中存储term在每个doc中的TF with pairs (docID, tf)

### 3. 选做
• 支持所有的SMART Notations

## **实现思路——排序索引模型**

一、 首先在实验一建立倒排索引的基础上，进行处理，建立了每一个term对应的 postings的结果，结果如实验一所示：

![2-rank1.png](https://i.loli.net/2019/10/20/ftVX7Jc9Ciz6Spd.png)



二、 在实验一的基础上，加上词频，即统计每一个文档内容的时候，记录在这一篇文档中词语的词频，mapper 即将term与相对应的text进行匹配，建立好索引 此时匹配的规则为  字典的 key为 lineNum:term, value为 [词频]，这样就得到了词频

```py
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

```


三、 开始结合词频，combiner 因为之前的出来的词频没有求和，现在是对每行词频进行求和，得到每行对应词频，开始将每个term对应的posting list进行合并，reducer，将之前的 字典 key为 lineNum:term, value为 [词频]，变为 key：term，value：[lineNum:词频]，和实验一操作一样，然后再实现排序，按term的首字母大小进行排序，从而建立起倒排索引，其中每一个term对应了 tweetid和在这一篇 tweetid中出现的词频, 与实验一处理类似

```py
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

#排序，返回一个列表
def shuffle(dic):
    dict = sorted(dic.items(), key=lambda x: x[0])
    return dict

```
<br>
在posting list中存储term在每个doc中的TF with pairs (docID, tf),每个词对应了 它出现的文档序号和在该文档下的词频

<br>

结果如下图所示：

![2-rank2.png](https://i.loli.net/2019/10/20/5AJKknVL9t8jwCI.png)

四、统计词出现的总词频和文档频率，也就是对 term来计算 包含的 tweetid数目即 文档频率，每个tweetid中出现的词频求和，即总词频

```py
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

```
五、对查询词 query，统计词频

```py
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

```
六、 计算 inc.itc

使用如图所示的算法：

![2-rank3.png](https://i.loli.net/2019/10/20/MAT8O6gKHv7cq4l.png)



首先循环query中出现的每一个词，计算出 词在query中的词频，词的逆文档频率，词在 tweetid中出现的词频，相乘，然后再对 词在tweetid出现的词频，求 l2范数(词向量在文档中的长度)，最后得出来 tf*idf 再除以 l2范数，得出最终的结果

```py
def do_RankSearch(query,doc,tdic):
    score={}
    length={}
    for term in query.keys():
        ll=query[term]
        ll=1+math.log(ll)  # query中的词频
        #print('ll: ',ll)
        if term in tdic.keys():  # 乘以 idf
           df=int(tdic[term][1])
         #  print('df: ',df)
           idf=math.log(30548/df)
           ll=ll*idf
         #  print('ll2: ',ll)
        if term in doc.keys():
            for postings in doc[term]:
                tweetid,tf=postings.split(':')
                tf=int(tf)
                tf = 1 + math.log(tf)
               # print('tf: ',tf)
                if tweetid  in score.keys():
                    score[tweetid]=score[tweetid]+ll*tf
                    length[tweetid]=length[tweetid]+tf**2
                else:
                    score[tweetid]=ll*tf
                    length[tweetid]=tf**2
    for tweetid in score.keys():
       score[tweetid]=score[tweetid]/math.sqrt(length[tweetid])


    return score


```
## **结果**  ##

以上是结果图，输入一个query，我会出现相应的分数

![2-rank5.png](https://i.loli.net/2019/10/20/YmgPX2UEhiaCQ4y.png)


为了比较结果，我专门把相应的text也输出，可以看到里面有 query中的单词


![2-rank4.png](https://i.loli.net/2019/10/20/lkZz1wU4RIGxJKS.png)






## **改进**

1. 使用textblob库，对倒排索引建立，还有query查询都进行了处理，对名词的单复数处理，对动词进行词性还原，这样提高了效果，让结果更具有一般性

```py
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

```



2. 加入了统计词频（tf）和 统计词的文档（df），求出 逆文档频率，并对结果进行了cosine 余弦函数归一化的处理，按照公式一步步得出，通过使用 Itc.Inc 模式，让结果更加正确

3. 在实验三中，我们使用 MAP，MRR，NDCG对实验二的查询结果进行了评价，具体结果请参照实验三，通过评价让查询的结果更加有说服力