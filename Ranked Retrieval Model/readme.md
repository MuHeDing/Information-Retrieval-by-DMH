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
<br>



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


结果图： 

每个词对应了 它出现的文档（此时用行号作为文档）和在该文档下的词频


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


```


## **实现思路——布尔查询**

1.要求能支持 and，or，not操作，现在已经能得到倒排索引

2.先得到输入的字符串，变成列表进行遍历，判断是否存在 and，or，not的词语

3.将结果 answer_set变成集合，分别对 and or not 操作进行处理

4.and即对应集合的交集 即 intersection函数，or即对应 集合的并集 即 union函数，not即对应集合的差集difference函数，通过这三个函数来实现布尔查询

and  和 not 单独操作

![boolean1.png](https://i.loli.net/2019/10/20/C52wX7hzxiBSReI.png)


and  和 not 同时操作


![boolean2.png](https://i.loli.net/2019/10/20/wmiWQMtyLVedf16.png)


and  or 和 not 同时操作

![boolean4.png](https://i.loli.net/2019/10/20/K2Jz6fQLWrNcsCT.png)


## **改进**

1. 增加了优先级操作，可以支持 A B C 三个单词之间的 and or not 的优先级操作，优先级关系为 not >  and > or

![boolean6.png](https://i.loli.net/2019/10/20/oUz3uvSZlyiQJ8F.png)

2. 学习和实用了 textblob库，实用了 其中 words方法就进行分词，还有对名词的单复数处理，对动词进行词性还原，学习实用的方法图片如下图所示：

![learn.png](https://i.loli.net/2019/10/20/3mIyoKnO49EqVLj.png)

3. 加入了统计词频（tf）和统计词的文档（df），便于实验2计算 文档和查询的分数