import re
import nltk
def token_stream(line):
    # re.I 不区分大小写
    li=nltk.word_tokenize(line)
    li=' '.join(li)
    return re.findall(r'\w+', li,re.I)  #返回一个列表

# 匹配
def mapper(lineNum, list):
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
# 结合 次数
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

def shuffle(dic):
    dict = sorted(dic.items(), key=lambda x: x[0])
    return dict


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
        if word == '':
            break
        list = token_stream(word)
        mdic = mapper(lineNum, list)
        #print(mdic)
        cdic = combiner(mdic)
        #print(cdic)
        rdic_p.update(cdic) #把cdic的键值赋值给 rdic_p

    rdic = reducer(rdic_p)

    # sdic = shuffle(rdic)
    # print(type(sdic))
    return rdic

if __name__ == '__main__':
    filepath="F:\\信息检索\\tweetsFor test.txt"
    rdic = get_reverse_index(filepath)
    dic=process(rdic)
   # print(dic)
    print(rdic)
    #print(dic)

    while(1):
        answer_set = set()
        search_word = input('Please input the word you want to search: ')
        if 'or' in search_word or 'OR' in search_word:
            Query =search_word.replace('or','',re.IGNORECASE)
            Q_word_list = Query.split()
            for word in Q_word_list:
                if word in dic.keys():
                    x=set(dic[word])
                    answer_set =answer_set.union(x)  # set or
            print(answer_set)

        elif 'and' in search_word or 'AND' in search_word:
            Query =search_word.replace('and','',re.IGNORECASE)

            Q_word_list = Query.split()
            i=0
            for word in Q_word_list:
                if word in dic.keys() and i==0:
                    x=set(dic[word])
                    answer_set=x
                    i = i + 1
                elif word in dic.keys() and i==1:
                    x = set(dic[word])
                    answer_set =answer_set.intersection(x)  # set or

            print(answer_set)
        elif 'not' in search_word or 'NOT' in search_word:
            Query =search_word.replace('not','',re.IGNORECASE)

            Q_word_list = Query.split()
            i=0
            for word in Q_word_list:
                if word in dic.keys() and i==0:
                    x=set(dic[word])
                    answer_set=x
                    i = i + 1
                elif word in dic.keys() and i==1:
                    x = set(dic[word])
                    answer_set.difference_update(x)

            print(answer_set)
        else:
            print(dic.get(search_word))


# # 查询
# while (1):
#     search_word = input('Please input the word you want to search: ')
#
#
#     else:
#         print(-1)