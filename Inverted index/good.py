import os
import re
import ast
import nltk
def token_stream(line):
    # re.I 不区分大小写
    li=nltk.word_tokenize(line)
    li=' '.join(li)
    return re.findall(r'\w+', li,re.I)

# 匹配
def mapper(lineNum, list):
    dic = {}
    for item in list:
        #print(item)
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
        ss = ''.join([lineNum, ':', str(dic.get(key))])
        if kk in rdic.keys():
            ll = rdic[kk]
            ll.append(ss)
            rdic[kk] = ll
        else:
            rdic[kk] = [ss]

    return rdic
# 结合
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

# def shuffle(dic):
#     dict = sorted(dic.items(), key=lambda x: x[0])
#     return dict

# def get_reverse_index(filepath):
#     file = open(filepath, 'r')
#     lineNum = 0
#     rdic_p = {}
#     while True:
#         lineNum += 1
#         content = file.readlines() #读入一行，返回一个字符串
#         #print(type(content))
#         word = d['text']
#         d = eval(t)
#         word = d['text']
#         if word != '':
#             pass
#         else:
#             break
#         list = token_stream(word)
#         #print(list)
#         mdic = mapper(lineNum, list)
#        # print(mdic)
#         cdic = combiner(mdic)
#         #print(cdic)
#         rdic_p.update(cdic) #把cdic的键值赋值给 rdic_p
#
#     rdic = reducer(rdic_p)
#
#     sdic = shuffle(rdic)
#     return sdic
def get_reverse_index(filepath):
    file = open(filepath, 'r')
    lineNum = 0
    rdic_p = {}
    for content in file.readlines():
        lineNum += 1
        d = eval(content)
        word = d['text']
        if word != '':
            pass
        else:
            break
        list = token_stream(word)
      #  print(list)
        mdic = mapper(lineNum, list)
       # print(mdic)
        cdic = combiner(mdic)
        #print(cdic)
        rdic_p.update(cdic) #把cdic的键值赋值给 rdic_p

    rdic = reducer(rdic_p)

    #sdic = shuffle(rdic)
    return rdic

if __name__ == '__main__':
    filepath="F:\\信息检索\\tweets.txt"
    dic = get_reverse_index(filepath)
    print(dic)
    # 查询
    # while(1):
    #     search_word = input('Please input the word you want to search: ')
    #
    #     if search_word in dic.keys():
    #         print(dic.get(search_word))
    #     else:
    #         print(-1)