# Information Retrieval—Evaluation

## **实验内容**

### **实现以下指标评价，并对HW1.2检索结果进行评价** ###
1. • Mean Average Precision (MAP)
2. • Mean Reciprocal Rank (MRR)
3. • Normalized Discounted Cumulative Gain (NDCG)

## **实现思路——评价模型**

一、 对实验二查询结果进行评价，首先提取查询内容，在MB171-225.txt中有查询内容，查询内容为标签<query></query>中的内容，如图所示：
<br>

![3-evaluation1.png](https://i.loli.net/2019/10/20/LBrbTx52g3oMZHO.png)

<br>

我们将查询内容提取出来，并输实验二排序检索模型中,得到 查询出来的 前K个 相关的 文档，写入 final_result.txt，然后进行评价

<br>

```py
    with open('F:\\信息检索\\evaluation\\final_result.txt', 'w', encoding='utf-8') as f_out:
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


```
<br>

二、 在这里，我顺便提一下 几个文件 其中 qrels.txt 即标准答案的输出结果文件，result.txt 即 将标准输出结果进行提取，然后再进行评价，可以得到 RightAnwerEvaluation.txt文件 ，即标准答案的结果，如下图所示：

<br>

![3-evaluation2.png](https://i.loli.net/2019/10/20/i89W2LoJ5sVckIP.png)


三、编写评价函数，MAP,MRR,NDCG

MAP，先得到qrels.txt 即标准答案的输出结果的 tweetid(docid)，再得到你的结果的 tweetid(docid),使用下图的公式，浏览每一项文档，分子为相关文档的个数，分母为浏览文档的个数，此时求出每一项的AP，最后再进行求均值 得到 MAP

<br>

![3-evaluation3.png](https://i.loli.net/2019/10/20/ezcV8qgBDGEiyuo.png)


代码如下：

<br>

```py
def MAP_eval(qrels_dict, test_dict, k = 100):
    AP_result = []
    file.write('MAP_evaluation: ' + '\n')
    for query in qrels_dict:
        test_result = test_dict[query] # 得到[docid,docid,docid,.......]
        true_list = set(qrels_dict[query].keys())  # 得到[docid,docid,docid,.......]
        #print(len(true_list))
        #length_use = min(k, len(test_result), len(true_list))
        length_use = min(k, len(test_result))
        if length_use <= 0:
            print('query ', query, ' not found test list')
            return []
        P_result = []
        i = 0
        i_retrieval_true = 0
        for doc_id in test_result[0: length_use]:
            i += 1
            if doc_id in true_list:
                i_retrieval_true += 1
                P_result.append(i_retrieval_true / i)
                #print(i_retrieval_true / i)
        if P_result:
            AP = np.sum(P_result) / len(true_list)
            print('query:', query, ',AP:', AP)
            file.write('query' + str(query) + ', AP: ' + str(AP)+'\n')
            AP_result.append(AP)
        else:
            print('query:', query, ' not found a true value')
            AP_result.append(0)
    MAP=np.mean(AP_result)
    file.write('MAP' + ' = ' + str(MAP) + '\n')
    return MAP

```
<br>

MRR，和MAP 步骤类似，使用倒数的方法，先得到qrels.txt 即标准答案的输出结果的 tweetid(docid)，再得到你的结果的 tweetid(docid),使用下图的公式，分子为一，分母为相关文档的位置，得到RR ，最后再对所有RR 求和


![3-evaluation4.png](https://i.loli.net/2019/10/20/dUpigE2qIeHYJhs.png)

代码如下：

<br>

```py
def MRR_eval(qrels_dict, test_dict, k = 100):
    RR_result = []
    file.write('\n')
    file.write('\n')
    file.write('MRR_evaluation: ' + '\n')
    for query in qrels_dict:
        test_result = test_dict[query] # 得到[docid,docid,docid,.......]
        true_list = set(qrels_dict[query].keys())  # 得到[docid,docid,docid,.......]
        length_use = min(k, len(test_result))
        if length_use <= 0:
            print('query ', query, ' not found test list')
            return []
        P_result = []
        i_retrieval_true = 0
        for doc_id in test_result[0: length_use]:
            if doc_id in true_list:
                i_retrieval_true += 1
                P_result.append(1/ i_retrieval_true)
        if P_result:
            RR = np.sum(P_result) / len(true_list)
            print('query:', query, ',RR:', RR)
            file.write('query' + str(query) + ', RR: ' + str(RR)+'\n')
            RR_result.append(RR)
        else:
            print('query:', query, ' not found a true value')
            RR_result.append(0)
    MRR=np.mean(RR_result)
    file.write('MRR' + ' = ' + str(MRR) + '\n')
    return MRR


```
<br>

NDCG: 先算 DCG 为累计的相关性之和,再除以 位置的以2为底的对数 , 算 IDCG 为 将从大到小排序之后的 DCG，然后再用下图 公式 求出 NDCG

![3-evaluation5.png](https://i.loli.net/2019/10/20/SEyGg43De9I1YMl.png)

代码如下：

<br>

```py
def NDCG_eval(qrels_dict, test_dict, k = 100):
    NDCG_result = []
    file.write('\n')
    file.write('\n')
    file.write('NDCG_evaluation: '+'\n')
    for query in qrels_dict:
        test_result = test_dict[query] # 得到[docid,docid,docid,.......]
        # calculate DCG just need to know the gains of groundtruth
        # that is [2,2,2,1,1,1]
        true_list = list(qrels_dict[query].values())
        true_list = sorted(true_list, reverse=True)
        i = 1
        DCG = 0.0
        IDCG = 0.0
        # maybe k is bigger than arr length
        length_use = min(k, len(test_result), len(true_list))
        if length_use <= 0:
            print('query ', query, ' not found test list')
            return []
        for doc_id in test_result[0: length_use]:
            i += 1
            rel = qrels_dict[query].get(doc_id, 0)
            DCG += (pow(2, rel) - 1) / math.log(i, 2)
            IDCG += (pow(2, true_list[i - 2]) - 1) / math.log(i, 2)
        NDCG = DCG / IDCG
        print('query', query, ', NDCG: ', NDCG)
        file.write('query'+str(query)+', NDCG: '+str(NDCG)+'\n')
        NDCG_result.append(NDCG)
    NDCG=np.mean(NDCG_result)
    file.write('NDCG' + ' = ' + str(NDCG) + '\n')
    return NDCG


```
<br>

四、输入我的结果final_result.txt 为171到225 所有查询词的 相关文档，我每个查询词取了100个，使用 上方的三种评价方式进行评价，MAP，MRR，NDCG得到结果



## **结果**  ##

每一个 query 中的 MAP 如下图，其余 MRR,NDCG 就不一一展示了

<br>

![3-evaluation6.png](https://i.loli.net/2019/10/20/KTdi5lgwZ9c6fpE.png)

最终求和之后：

<br>

![3-evaluation7.png](https://i.loli.net/2019/10/20/LRelKviBmSaPyfX.png)

结果比 标准答案小了一些，但基本上接近，实现的查询是有效的

## **改进**

1. 使用textblob库，对 query查询都进行了处理，对名词的单复数处理，对动词进行词性还原，这样提高了效果，让结果更具有一般性

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

2. 加入了统计词频（tf）和 统计词的文档（df），求出 逆文档频率，并对结果进行了cosine 余弦函数归一化的处理，通过使用 Itc.Inc 模式，大幅度提高了结果，比使用普通的对 按照出现的query中词个数之和排序的效果要好很多
