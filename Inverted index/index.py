import re
from textblob import TextBlob
from textblob import Word
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
# 结合 词频
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


def get_reverse_index(filepath):
    file = open(filepath, 'r')
    lineNum = 0
    rdic_p = {}
    for content in file.readlines():
        lineNum += 1
        d = eval(content) #变成字典
        word = d['text']
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
    return dict(sdic)




if __name__ == '__main__':
    filepath="F:\\信息检索\\tweets.txt"
    rdic = get_reverse_index(filepath)
    #print(rdic)
    dic=process(rdic)

    search_word=' '
    while(search_word!='q'):
        answer_set = set()
        search_word = input('Please input the word you want to search (all lower):  ')
        search_word=search_word.lower()
        word_list=search_word.split()
        #普通的优先级判断
        if len(word_list)==5:
            # A and B or C
            if (word_list[1] == "and") and (word_list[3] == "or"):
                answer_set=dict[word_list[0]]
                answer_set.intersection_update(dict[word_list[2]])
                answer_set=answer_set.union(dict[word_list[4]])
            # A - B or C
            elif (word_list[1] == "not") and (word_list[3] == "or"):
                answer_set=dict[word_list[0]]
                answer_set.difference_update(dict[word_list[2]])
                answer_set=answer_set.union(dict[word_list[4]])
            # A or B and C
            elif (word_list[1] == "or") and (word_list[3] == "and"):
                answer_set = dict[word_list[2]]
                answer_set.intersection_update(dict[word_list[4]])
                answer_set = answer_set.union(dict[word_list[0]])
            # A or B - C
            elif (word_list[1] == "or") and (word_list[3] == "not"):
                answer_set = dict[word_list[2]]
                answer_set.difference_update(dict[word_list[4]])
                answer_set = answer_set.union(dict[word_list[0]])
        for i,word in enumerate(word_list):
            if word in dic.keys() and i==0:
                answer_set=set(dic[word])
            elif i%2==1 and i!=len(word_list)-1:
                if word=='and':
                    if word_list[i+1] in dic.keys():
                        x=set(dic[word_list[i+1]])
                        answer_set.intersection_update(x)
                if word=='or':
                    if word_list[i+1] in dic.keys():
                        x=set(dic[word_list[i+1]])
                        answer_set=answer_set.union(x)

                if word=='not':
                    if word_list[i + 1] in dic.keys():
                        x = set(dic[word_list[i + 1]])
                        answer_set.difference_update(x)
        print(answer_set)



        # if 'or' in search_word or 'OR' in search_word:
        #     Query =search_word.replace('or','',re.IGNORECASE)
        #     Q_word_list = Query.split()
        #     for word in Q_word_list:
        #         if word in dic.keys():
        #             x=set(dic[word])
        #             answer_set =answer_set.union(x)  # set or
        #     print(answer_set)
        #
        # elif 'and' in search_word or 'AND' in search_word:
        #     Query =search_word.replace('and','',re.IGNORECASE)
        #
        #     Q_word_list = Query.split()
        #     i=0
        #     for word in Q_word_list:
        #         if word in dic.keys() and i==0:
        #             x=set(dic[word])
        #             answer_set=x
        #             i = i + 1
        #         elif word in dic.keys() and i==1:
        #             x = set(dic[word])
        #             answer_set =answer_set.intersection(x)  # set or
        #
        #     print(answer_set)
        # elif 'not' in search_word or 'NOT' in search_word:
        #     Query =search_word.replace('not','',re.IGNORECASE)
        #
        #     Q_word_list = Query.split()
        #     i=0
        #     for word in Q_word_list:
        #         if word in dic.keys() and i==0:
        #             x=set(dic[word])
        #             answer_set=x
        #             i = i + 1
        #         elif word in dic.keys() and i==1:
        #             x = set(dic[word])
        #             answer_set.difference_update(x)
        #
        #     print(answer_set)
        # else:
        #     print(dic.get(search_word))
