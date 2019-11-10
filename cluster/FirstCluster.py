from sklearn.cluster import KMeans
from sklearn import datasets
from sklearn.preprocessing import scale
from sklearn.cluster import AffinityPropagation
import numpy as np
from sklearn import metrics
from time import time
from sklearn.cluster import estimate_bandwidth
from sklearn.cluster import MeanShift
from sklearn.cluster import SpectralClustering
from sklearn.cluster import spectral_clustering
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import DBSCAN
from sklearn.cluster import OPTICS
from sklearn import mixture
from sklearn.cluster import Birch
from sklearn.decomposition import PCA
# 手写数字识别
digits = datasets.load_digits()
#print(digits.data.shape)  # 1797*64,每一张是一个 64像素的矩阵

data = scale(digits.data)  # newX = (X- 均值) / 标准差
#print(data)
n_digits=len(np.unique(digits.target))
sample_size = 300
labels = digits.target
print('init\t\ttime\tinertia\thomo\tcompl\tv-meas\tARI\tAMI\tsilhouette')
def bench_k_means(estimator, name, data):
    t0 = time()
    estimator.fit(data)
    print('%-9s\t%.2fs\t%i\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f'
          % (name, (time() - t0), estimator.inertia_,
             metrics.homogeneity_score(labels, estimator.labels_),
             metrics.completeness_score(labels, estimator.labels_),
             metrics.v_measure_score(labels, estimator.labels_),
             metrics.adjusted_rand_score(labels, estimator.labels_),
             metrics.adjusted_mutual_info_score(labels,  estimator.labels_,
                                                average_method='arithmetic'),
             metrics.silhouette_score(data, estimator.labels_,
                                      metric='euclidean',
                                      sample_size=sample_size)))
def bench_show(estimator, name, data):
    t0 = time()
    estimator.fit(data)
    print('%-9s\t%.2fs\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f'
          % (name, (time() - t0),
             metrics.homogeneity_score(labels, estimator.labels_),
             metrics.completeness_score(labels, estimator.labels_),
             metrics.v_measure_score(labels, estimator.labels_),
             metrics.adjusted_rand_score(labels, estimator.labels_),
             metrics.adjusted_mutual_info_score(labels,  estimator.labels_,
                                                average_method='arithmetic'),
             metrics.silhouette_score(data, estimator.labels_,
                                      metric='euclidean',
                                      sample_size=sample_size)))
def bench_show2(estimator, name, data):
    t0 = time()
    estimator.fit(data)
    print('%-9s\t%.2fs\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f'
          % (name, (time() - t0),
             metrics.homogeneity_score(labels, estimator.predict(data)),
             metrics.completeness_score(labels, estimator.predict(data)),
             metrics.v_measure_score(labels, estimator.predict(data)),
             metrics.adjusted_rand_score(labels, estimator.predict(data)),
             metrics.adjusted_mutual_info_score(labels,  estimator.predict(data),
                                                average_method='arithmetic'),
             metrics.silhouette_score(data, estimator.predict(data),
                                      metric='euclidean',
                                      sample_size=sample_size)))

def bench_show3(estimator, name, data):
    t0 = time()
    estimator.fit(data)
    print('%-9s\t%.2fs\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f'
          % (name, (time() - t0),
             metrics.homogeneity_score(labels, estimator.labels_),
             metrics.completeness_score(labels, estimator.labels_),
             metrics.v_measure_score(labels, estimator.labels_),
             metrics.adjusted_rand_score(labels, estimator.labels_),
             metrics.adjusted_mutual_info_score(labels,  estimator.labels_,
                                                average_method='arithmetic')))
# estimator=KMeans(init='k-means++', n_clusters=n_digits, n_init=10)
# estimator.fit(data)
# #z=estimator.predict(data)
# z=estimator.labels_

# score=metrics.normalized_mutual_info_score(digits.target,z,average_method='arithmetic')
# print(score)
#
bench_k_means(KMeans(init='k-means++', n_clusters=n_digits, n_init=10),
              name="k-means++", data=data)
# 相似性传播
af = AffinityPropagation().fit(data)
#
# score=metrics.normalized_mutual_info_score(digits.target,af.labels_,average_method='arithmetic')
# print(score)
bench_show(AffinityPropagation(),
              name="AffinityPropagation", data=data)
# 均值漂移
bandwidth = estimate_bandwidth(data,quantile=0.2,n_samples=500)
ms = MeanShift(bandwidth=bandwidth,bin_seeding=True)
# ms.fit(data)
# print(ms.labels_)
# score=metrics.normalized_mutual_info_score(digits.target,ms.labels_,average_method='arithmetic')
# print(score)
bench_show(MeanShift(bandwidth=bandwidth,bin_seeding=True),
              name="MeanShift", data=data)
#光谱聚类
#spectral = SpectralClustering(n_clusters=n_digits,eigen_solver='arpack').fit(data)
#sc = SpectralClustering(n_digits, affinity='precomputed', n_init=100).fit_predict(data)
pca=PCA(n_components=n_digits).fit_transform(data)
#score=metrics.normalized_mutual_info_score(digits.target,sc.labels_,average_method='arithmetic')
#print(score)
bench_show3(SpectralClustering(n_digits),name="SpectralClustering", data=pca)
# 分层聚类
#ward = AgglomerativeClustering(n_clusters=n_digits, linkage='ward')
# ward.fit(data)
# score=metrics.normalized_mutual_info_score(digits.target,ward.labels_,average_method='arithmetic')
# print(score)
bench_show( AgglomerativeClustering(n_clusters=n_digits, linkage='ward'),
              name="AgglomerativeClustering", data=data)
# 基于密度的聚类
# db = DBSCAN().fit(data)

# score=metrics.normalized_mutual_info_score(digits.target,db.labels_,average_method='arithmetic')
# print(score)
bench_show3(DBSCAN(),name="DBSCAN", data=data)


# 光学聚类
# clust = OPTICS(min_samples=50, xi=.05, min_cluster_size=.05)
#
# # Run the fit
# clust.fit(data)
# score=metrics.normalized_mutual_info_score(digits.target,clust.labels_,average_method='arithmetic')
# print(score)

bench_show(OPTICS(min_samples=50, xi=.05, min_cluster_size=.05),name="OPTICS", data=data)

# 高斯混合模型
#gmm = mixture.GaussianMixture(n_components=n_digits, covariance_type='full').fit(data)
# score=metrics.normalized_mutual_info_score(digits.target,gmm.predict(data),average_method='arithmetic')
# print(score)

bench_show2(mixture.GaussianMixture(n_components=n_digits, covariance_type='full'),name="Gaussian", data=data)

# 桦木
# brc = Birch(branching_factor=50, n_clusters=n_digits, threshold=0.5, compute_labels=True)
# brc.fit(data)
# score=metrics.normalized_mutual_info_score(digits.target,brc.labels_,average_method='arithmetic')
# print(score)

bench_show2(Birch(branching_factor=50, n_clusters=n_digits, threshold=0.5, compute_labels=True),name="Birch", data=data)

