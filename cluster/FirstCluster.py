from sklearn.cluster import KMeans
from sklearn import datasets
from sklearn.preprocessing import scale
from sklearn.cluster import AffinityPropagation
import numpy as np
from sklearn import metrics
from sklearn.cluster import estimate_bandwidth
from sklearn.cluster import MeanShift
from sklearn.cluster import SpectralClustering
from sklearn.cluster import spectral_clustering
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import DBSCAN
from sklearn.cluster import OPTICS
from sklearn import mixture
from sklearn.cluster import Birch
# 手写数字识别
digits = datasets.load_digits()
#print(digits.data.shape)  # 1797*64,每一张是一个 64像素的矩阵

data = scale(digits.data)  # newX = (X- 均值) / 标准差
#print(data)
n_digits=len(np.unique(digits.target))

# estimator=KMeans(init='k-means++', n_clusters=n_digits, n_init=10)
# estimator.fit(data)
# #z=estimator.predict(data)
# z=estimator.labels_
# count=0
# for i in range(0,len(digits.data)):
#     if digits.target[i]==z[i]:
#         # print(digits.target[i])
#         # print(z[i])
#         count=count+1
# print(count)
# score=metrics.normalized_mutual_info_score(digits.target,z,average_method='arithmetic')
# print(score)
#

# 相似性传播
# af = AffinityPropagation().fit(data)
#
# score=metrics.normalized_mutual_info_score(digits.target,af.labels_,average_method='arithmetic')
# print(score)

# 均值漂移
# bandwidth = estimate_bandwidth(data,quantile=0.2,n_samples=500)
# ms = MeanShift(bandwidth=bandwidth,bin_seeding=True)
# ms.fit(data)
# print(ms.labels_)
# score=metrics.normalized_mutual_info_score(digits.target,ms.labels_,average_method='arithmetic')
# print(score)

#光谱聚类
# 有问题
#spectral = SpectralClustering(n_clusters=n_digits,eigen_solver='arpack').fit(data)
# sc = SpectralClustering(n_digits, affinity='precomputed', n_init=100).fit_predict(data)
# score=metrics.normalized_mutual_info_score(digits.target,sc.labels_,average_method='arithmetic')
# print(score)

# 分层聚类
# ward = AgglomerativeClustering(n_clusters=n_digits, linkage='ward')
# ward.fit(data)
# score=metrics.normalized_mutual_info_score(digits.target,ward.labels_,average_method='arithmetic')
# print(score)

# 基于密度的聚类
# db = DBSCAN().fit(data)
# score=metrics.normalized_mutual_info_score(digits.target,db.labels_,average_method='arithmetic')
# print(score)

# 光学聚类
# clust = OPTICS(min_samples=50, xi=.05, min_cluster_size=.05)
#
# # Run the fit
# clust.fit(data)
# score=metrics.normalized_mutual_info_score(digits.target,clust.labels_,average_method='arithmetic')
# print(score)

# 高斯混合模型
# gmm = mixture.GaussianMixture(n_components=n_digits, covariance_type='full').fit(data)
# score=metrics.normalized_mutual_info_score(digits.target,gmm.predict(data),average_method='arithmetic')
# print(score)

# 桦木
brc = Birch(branching_factor=50, n_clusters=n_digits, threshold=0.5, compute_labels=True)
brc.fit(data)
score=metrics.normalized_mutual_info_score(digits.target,brc.labels_,average_method='arithmetic')
print(score)

