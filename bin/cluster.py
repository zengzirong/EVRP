import numpy as np
from sklearn.cluster import KMeans,DBSCAN,OPTICS,SpectralClustering,AgglomerativeClustering,MeanShift,Birch
from sklearn.mixture import GaussianMixture
from readData import getclu

from random import shuffle

def shuffle_result(labels, n):
    n = n if n > 0 else 1
    res = [[] for i in range(n)]
    for i in range(len(labels)): res[labels[i]].append(i + 1)
    for i in range(n): shuffle(res[i])
    shuffle(res)
    return np.hstack(res)
def KMeans_construction():
    numpair,data, n_clusters = getclu()
    da = [[d['x'], d['y']] for d in data]
    kmeans = KMeans(n_clusters=n_clusters).fit(da)
    labels = kmeans.labels_
    return shuffle_result(labels, max(labels)+1)

def OPTICS_construction():
    numpair,data, n_clusters = getclu()

    min_samples = 5
    da = [[d['x'], d['y']] for d in data]
    optics = OPTICS(min_samples=min_samples).fit(da)
    labels = optics.labels_
    return shuffle_result(labels, max(labels) + 1)

def DBSCAN_construction(data, eps=0.5, min_samples=5, metric='euclidean', metric_params=None, algorithm='auto',leaf_size=30, p=None):
    data = [[d['x'], d['y']] for d in data]
    dbscan = DBSCAN(eps,  # 邻域半径
           min_samples,  # 最小样本点数，MinPts
           metric,
           metric_params,
           algorithm,  # 'auto','ball_tree','kd_tree','brute',4个可选的参数 寻找最近邻点的算法，例如直接密度可达的点
           leaf_size,  # balltree,cdtree的参数
           p).fit(data)
    # 噪声点的label会被置为-1，这一项要不要筛掉？
    labels = dbscan.labels_
    return shuffle_result(labels, max(labels)+1)



def Spectral_construction():
    numpair,data, n_clusters = getclu()
    da = [[d['x'], d['y']] for d in data]
    spectral = SpectralClustering(n_clusters=n_clusters).fit(da)
    labels = spectral.labels_
    return shuffle_result(labels, max(labels) + 1)

def Agglomerative_construction():   # 这个其实就是KNN，和KNN的思路一致
    numpair,data, n_clusters = getclu()
    da = [[d['x'], d['y']] for d in data]
    agglomerative = AgglomerativeClustering(n_clusters=n_clusters).fit(da)
    labels = agglomerative.labels_
    return shuffle_result(labels, max(labels) + 1)

def MeanShift_construction():
    bandwidth = 10
    numpair,data, n_clusters = getclu()
    da = [[d['x'], d['y']] for d in data]
    meanshift = MeanShift(bandwidth=bandwidth).fit(da)
    labels = meanshift.labels_
    return shuffle_result(labels, max(labels) + 1)

def Birch_construction():
    numpair,data, n_clusters = getclu()
    da = [[d['x'], d['y']] for d in data]
    birch = Birch(n_clusters=n_clusters).fit(da)
    labels = birch.labels_
    return shuffle_result(labels, max(labels) + 1)

def GaussianMixture_construction( ):
    random_state = 0
    n_components = 2
    global data, n_clusters
    da = [[d['x'], d['y']] for d in data]
    gaussian = GaussianMixture(n_components=n_components, random_state=random_state).fit(da)
    labels = gaussian.predict(da)
    return shuffle_result(labels, max(labels) + 1)

if __name__ == '__main__':
    '''
    data = [
        {'x': 1, 'y': 2},
        {'x': 2, 'y': 1},
        {'x': 3, 'y': 1},
        {'x': 5, 'y': 4},
        {'x': 2, 'y': 3},
        {'x': 4, 'y': 2}
    ]
    p = []
    p.append(0)
    a = KMeans_construction(data, n_clusters=3)
    for i in a:
        p.append(i)
    print(p)
    '''
    # print(DBSCAN_construction(data, eps=0.5,
    #                           min_samples=5,
    #                           metric='euclidean',
    #                           metric_params=None,
    #                           algorithm='auto',
    #                           leaf_size=30,
    #                           p=None))   # 这个不建议使用，很容易将数据监测为噪声点，然后都label都被设置为-1
    # print(OPTICS_construction(data, min_samples=5))
    # print(Spectral_construction(data))
    # print(Agglomerative_construction(data, n_clusters=3))
    # print(MeanShift_construction(data, bandwidth=2))
    # print(Birch_construction(data, n_clusters=3))
    # print(GaussianMixture_construction(data, n_components=2, random_state=0))
