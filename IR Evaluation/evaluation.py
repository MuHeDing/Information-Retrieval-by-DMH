import math
import numpy as np
# 我的结果
myevaluationfilename='F:\\信息检索\\evaluation\\final_result_evaluation.txt'
# 正确的结果
goodevaluationfilename='F:\\信息检索\\evaluation\\Goodevaluationresult.txt'
file = open(myevaluationfilename, 'w', encoding='utf-8')
def generate_tweetid_gain(file_name):
    qrels_dict = {}
    with open(file_name, 'r', errors='ignore') as f:
        for line in f:
            ele = line.strip().split(' ')
            if ele[0] not in qrels_dict:
                qrels_dict[ele[0]] = {}
            # here we want the gain of doc_id in qrels_dict > 0,
            # so it's sorted values can be IDCG groundtruth
            if int(ele[3]) > 0:
                qrels_dict[ele[0]][ele[2]] = int(ele[3]) # 字典进行嵌套
        #print(qrels_dict)
    return qrels_dict

def read_tweetid_test(file_name):
    # input file format
    # query_id doc_id
    # query_id doc_id
    # query_id doc_id
    # ...
    test_dict = {}
    with open(file_name, 'r', errors='ignore') as f:
        for line in f:
            ele = line.strip().split(' ')
            if ele[0] not in test_dict:
                test_dict[ele[0]] = []
            test_dict[ele[0]].append(ele[1])
    return test_dict
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

def evaluation():
    k = 100
    # query relevance file
    file_qrels_path = 'qrels.txt'
    # qrels_dict = {query_id:{doc_id:gain, doc_id:gain, ...}, ...}
    qrels_dict = generate_tweetid_gain(file_qrels_path)
    # ur result, format is in function read_tweetid_test, or u can write by ur own
    # 我的结果
    myfile_test_path = 'F:\\信息检索\\evaluation\\final_result.txt'
    #正确结果
    goodfile_test_path='result.txt'
    # test_dict = {query_id:[doc_id, doc_id, ...], ...}
    test_dict = read_tweetid_test(myfile_test_path)


    MAP = MAP_eval(qrels_dict, test_dict, k)
    print('MAP', ' = ', MAP, sep='')
    MRR = MRR_eval(qrels_dict, test_dict, k)
    print('MRR', ' = ', MRR, sep='')
    NDCG = NDCG_eval(qrels_dict, test_dict, k)
    print('NDCG', ' = ', NDCG, sep='')
    file.close()
if __name__ == '__main__':
    evaluation()
