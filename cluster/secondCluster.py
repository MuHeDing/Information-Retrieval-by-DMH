

from sklearn.datasets import fetch_20newsgroups
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer
from sklearn.cluster import AffinityPropagation
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

from sklearn.cluster import KMeans, MiniBatchKMeans
from sklearn.decomposition import PCA
import logging
from optparse import OptionParser
import sys
from time import time

import numpy as np


# Display progress logs on stdout
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')

# parse commandline arguments
op = OptionParser()
op.add_option("--lsa",
              dest="n_components", type="int",
              help="Preprocess documents with latent semantic analysis.")
op.add_option("--no-minibatch",
              action="store_false", dest="minibatch", default=True,
              help="Use ordinary k-means algorithm (in batch mode).")
op.add_option("--no-idf",
              action="store_false", dest="use_idf", default=True,
              help="Disable Inverse Document Frequency feature weighting.")
op.add_option("--use-hashing",
              action="store_true", default=False,
              help="Use a hashing feature vectorizer")
op.add_option("--n-features", type=int, default=10000,
              help="Maximum number of features (dimensions)"
                   " to extract from text.")
op.add_option("--verbose",
              action="store_true", dest="verbose", default=False,
              help="Print progress reports inside k-means algorithm.")

print(__doc__)
op.print_help()


def is_interactive():
    return not hasattr(sys.modules['__main__'], '__file__')


# work-around for Jupyter notebook and IPython console
argv = [] if is_interactive() else sys.argv[1:]
(opts, args) = op.parse_args(argv)
if len(args) > 0:
    op.error("this script takes no arguments.")
    sys.exit(1)


# #############################################################################
# Load some categories from the training set
categories = [
    'alt.atheism',
    'talk.religion.misc',
    'comp.graphics',
    'sci.space',
]
# Uncomment the following to do the analysis on all the categories
# categories = None

print("Loading 20 newsgroups dataset for categories:")
print(categories)

dataset = fetch_20newsgroups(subset='all', categories=categories,
                             shuffle=True, random_state=42)

print("%d documents" % len(dataset.data))
print("%d categories" % len(dataset.target_names))
print()

labels = dataset.target
#print(labels.shape)  #3387

true_k = np.unique(labels).shape[0]
print("Extracting features from the training dataset "
      "using a sparse vectorizer")
t0 = time()
# 文本向量化
# 使用哈希文本向量化
if opts.use_hashing:
    if opts.use_idf:
        # Perform an IDF normalization on the output of HashingVectorizer
        hasher = HashingVectorizer(n_features=opts.n_features,
                                   stop_words='english', alternate_sign=False,
                                   norm=None, binary=False)
        vectorizer = make_pipeline(hasher, TfidfTransformer())
    else:
        vectorizer = HashingVectorizer(n_features=opts.n_features,
                                       stop_words='english',
                                       alternate_sign=False, norm='l2',
                                       binary=False)
# 使用tf-idf文本向量化
else:
    vectorizer = TfidfVectorizer(max_df=0.5, max_features=opts.n_features,
                                 min_df=2, stop_words='english',
                                 use_idf=opts.use_idf)
X = vectorizer.fit_transform(dataset.data)

print("done in %fs" % (time() - t0))
print("n_samples: %d, n_features: %d" % X.shape)
print()

#print(X)

n_digits=len(categories)

# if opts.n_components:
#     print("Performing dimensionality reduction using LSA")
#     t0 = time()
#     # Vectorizer results are normalized, which makes KMeans behave as
#     # spherical k-means for better results. Since LSA/SVD results are
#     # not normalized, we have to redo the normalization.
#     svd = TruncatedSVD(opts.n_components)
#     normalizer = Normalizer(copy=False)
#     lsa = make_pipeline(svd, normalizer)
#
#     X = lsa.fit_transform(X)
#
#     print("done in %fs" % (time() - t0))
#
#     explained_variance = svd.explained_variance_ratio_.sum()
#     print("Explained variance of the SVD step: {}%".format(
#         int(explained_variance * 100)))
#
#     print()

# Vectorizer results are normalized, which makes KMeans behave as
# spherical k-means for better results. Since LSA/SVD results are
# not normalized, we have to redo the normalization.
def decompostion(X):
    svd = TruncatedSVD(n_digits)
    normalizer = Normalizer(copy=False)
    lsa = make_pipeline(svd, normalizer)

    X = lsa.fit_transform(X)

    # print("done in %fs" % (time() - t0))
    #
    # explained_variance = svd.explained_variance_ratio_.sum()
    # print("Explained variance of the SVD step: {}%".format(
    #     int(explained_variance * 100)))
    return X

def bench_k_means(estimator, name, data):
    t0 = time()
    estimator.fit(data)
    print('%-9s\t%.2fs\t%i\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f'
          % (name, (time() - t0), estimator.inertia_,
             metrics.homogeneity_score(labels, estimator.labels_),
             metrics.completeness_score(labels, estimator.labels_),
             metrics.v_measure_score(labels, estimator.labels_),
             metrics.adjusted_rand_score(labels, estimator.labels_),
             metrics.silhouette_score(data, estimator.labels_,
                                      metric='euclidean',
                                      sample_size=10000)))
def bench_show(estimator, name, data):
    t0 = time()
    estimator.fit(data)
    print('%-9s\t%.2fs\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f'
          % (name, (time() - t0),
             metrics.homogeneity_score(labels, estimator.labels_),
             metrics.completeness_score(labels, estimator.labels_),
             metrics.v_measure_score(labels, estimator.labels_),
             metrics.adjusted_rand_score(labels, estimator.labels_),
             metrics.silhouette_score(data, estimator.labels_,
                                      metric='euclidean',
                                      sample_size=1000)))
def bench_show2(estimator, name, data):
    t0 = time()
    estimator.fit(data)
    print('%-9s\t%.2fs\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f'
          % (name, (time() - t0),
             metrics.homogeneity_score(labels, estimator.predict(data)),
             metrics.completeness_score(labels, estimator.predict(data)),
             metrics.v_measure_score(labels, estimator.predict(data)),
             metrics.adjusted_rand_score(labels, estimator.predict(data)),
             metrics.silhouette_score(data, estimator.predict(data),
                                      metric='euclidean',
                                      sample_size=1000)))

def bench_show3(estimator, name, data):
    t0 = time()
    estimator.fit(data)
    print('%-9s\t%.2fs\t%.3f\t%.3f\t%.3f\t%.3f'
          % (name, (time() - t0),
             metrics.homogeneity_score(labels, estimator.labels_),
             metrics.completeness_score(labels, estimator.labels_),
             metrics.v_measure_score(labels, estimator.labels_),
             metrics.adjusted_rand_score(labels, estimator.labels_)))




print('init\t\ttime\tinertia\thomo\tcompl\tv-meas\tARI\tAMI\tsilhouette')
km=MiniBatchKMeans(n_clusters=true_k, init='k-means++', n_init=1,
                          init_size=1000, batch_size=1000, verbose=opts.verbose)

bench_k_means(km,name="k-means++", data=X)


# 相似性传播,没有压缩
bench_show(AffinityPropagation(),name="AffinityPropagation",data=X)


# 均值漂移 进行压缩
bandwidth = estimate_bandwidth(decompostion(X), quantile=0.2, n_samples=500)
bench_show(MeanShift(bandwidth=bandwidth,bin_seeding=True),
              name="MeanShift", data=decompostion(X))


# 光谱聚类 压缩
bench_show3(SpectralClustering(n_digits),
              name="MeanShift", data=decompostion(X))

# 分层聚类，进行了压缩
# AgglomerativeClustering(n_clusters=n_digits, linkage='ward')
bench_show(AgglomerativeClustering(n_clusters=n_digits, linkage='ward'),name="AgglomerativeClustering", data=decompostion(X))
# 密度聚类 不需要压缩
# km=DBSCAN()
bench_show3(DBSCAN(),name="DBSCAN",data=X)

#  光学聚类 而且需要压缩

bench_show(OPTICS(),name="OPTICS", data=decompostion(X))

# 高斯混合模型 进行压缩
bench_show2(mixture.GaussianMixture(n_components=n_digits, covariance_type='full'),name="Gaussian", data=decompostion(X))
#km=Birch(branching_factor=50, n_clusters=n_digits, threshold=0.5, compute_labels=True)
# X=decompostion(X)  #0.561 0.590 0.575 0.565 0.469
# 桦木 进行压缩
bench_show2(Birch(branching_factor=50, n_clusters=n_digits, threshold=0.5, compute_labels=True),name="Birch", data=decompostion(X))



if not opts.use_hashing:
    print("Top terms per cluster:")

    if opts.n_components:
        original_space_centroids = svd.inverse_transform(km.cluster_centers_)
        order_centroids = original_space_centroids.argsort()[:, ::-1]
    else:
        order_centroids = km.cluster_centers_.argsort()[:, ::-1]

    terms = vectorizer.get_feature_names()
    for i in range(true_k):
        print("Cluster %d:" % i, end='')
        for ind in order_centroids[i, :10]:
            print(' %s' % terms[ind], end='')
        print()