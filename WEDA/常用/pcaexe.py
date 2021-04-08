from sklearn.decomposition import PCA
from sklearn.datasets.samples_generator import make_blobs
import numpy as np

x, y = make_blobs(n_features = 4900, n_samples = 204)


pca = PCA(n_components = 500)
pca.fit_transform(x)




