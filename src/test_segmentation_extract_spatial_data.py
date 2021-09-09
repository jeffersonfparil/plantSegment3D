### test segmentation and extraction of spatial colorimetric data
import os
import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt
import random

os.chdir("/home/jeff/Documents/plantSegment3D/")
from src.ply_reader import read_ply

### extract data
data = read_ply("res/Lr_test.ply")
# data = read_ply("res/Lr_plates.ply")
# data = read_ply("res/At_test.ply")
X = data['points'] ### extract datapoints as pandas array

### invert z orientation so that the tray isn't upsidedown by default
z_max = max(X["z"])
z_min = min(X["z"])
z_new = (abs(1-((X["z"] - z_min)/(z_max - z_min))) * (z_max - z_min)) + z_min
X["z"] = z_new

### some traits/methods/properties of the numpy array
X.shape
X.columns
X.dtypes
X.index
X.head(10)
X.tail(10)
X.describe()
X["red"]
X[["x","y","z"]]
X.iloc[0]
X.iloc[0:5]
X.iloc[0:5, 5:8]
X.iloc[0:10, :]

### subset to include only the releveant chuck along the z-axis
X = X[(X["z"]>1050)][(X["z"]<1200)]

### convert pandas array into numpy array then into open3d object, plot and save
COORDINATES = X[["x", "y", "z"]]
COLOURS = X[["red", "green", "blue"]]/255
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(COORDINATES.to_numpy())
pcd.colors = o3d.utility.Vector3dVector(COLOURS.to_numpy())

### plot
o3d.visualization.draw_geometries([pcd], point_show_normal=True)

### segmentation with DBSCAN (Density-based spatial clustering of applications with noise)
labels = np.array(pcd.cluster_dbscan(eps=7, min_points=10))

max_label = labels.max()
colors = plt.get_cmap("tab20")(labels / (max_label if max_label > 0 else 1))

colors[labels < 0] = 0
pcd.colors = o3d.utility.Vector3dVector(colors[:, :3])
o3d.visualization.draw_geometries([pcd])

###@@@ Note that we need to find the most appropriate epsilon heuristically!
###@@@ Probably by taking a look at the distribution of Euclidean distances between points?!

### sample a small number of random points for efficiency

n_rand = 1000
idx_rand = random.sample(list(range(0, X.shape[0])), n_rand)

A = COORDINATES.iloc[idx_rand[0:round(n_rand/2)], :]
B = COORDINATES.iloc[idx_rand[round(n_rand/2):n_rand], :]
D = np.sqrt(np.sum(np.square(np.subtract(A, B)), axis=1).tolist())
np.mean(D)
np.std(D)
plt.hist(D)
plt.show()

epsilon = np.std(D) / 12 ### divide by the expected number of cells
labels = np.array(pcd.cluster_dbscan(eps=epsilon, min_points=10))

max_label = labels.max()
colors = plt.get_cmap("tab20")(labels / (max_label if max_label > 0 else 1))

colors[labels < 0] = 0
pcd.colors = o3d.utility.Vector3dVector(colors[:, :3])
o3d.visualization.draw_geometries([pcd])

### not precise enough!
### will need to use a colour-based thresholding, probably a combination of greeness, NIR and NDVI
### but we have to make sure we're not biasing the dataset by discarding the dead tissues!!!!






### rewrite output ply file
o3d.io.write_point_cloud("test_rewrite_RGB_At.ply", pcd)

### visualise NIR
NIR = COLOURS
NIR["red"] = X["nir"]/255
NIR["green"] = 0
NIR["blue"] = 0
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(COORDINATES.to_numpy())
pcd.colors = o3d.utility.Vector3dVector(NIR.to_numpy())
o3d.visualization.draw_geometries([pcd], point_show_normal=True)

### visualise NDVI
NDVI = COLOURS
NDVI["red"] = 0
NDVI["green"] = X["ndvi"]/255
NDVI["blue"] = 0
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(COORDINATES.to_numpy())
pcd.colors = o3d.utility.Vector3dVector(NDVI.to_numpy())
o3d.visualization.draw_geometries([pcd], point_show_normal=True)

### set an NDVI threshold
plt.hist(x=NDVI["green"].to_numpy())
plt.show()
ndvi_threshold = 0.8
NDVI[NDVI["green"] < ndvi_threshold] = 0
NDVI = NDVI[NDVI!=0]

pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(COORDINATES.to_numpy())
pcd.colors = o3d.utility.Vector3dVector(NDVI.to_numpy())
o3d.visualization.draw_geometries([pcd], point_show_normal=True)

### Notice that we've gotten rid of the plastic labels!




###@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
###@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
###@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
### test lolium
data = read_ply("res/Lr_test.ply")
X = data['points'] ### extract datapoints as pandas array
### invert z orientation so that the tray isn't upsidedown by default
z_max = max(X["z"])
z_min = min(X["z"])
z_new = (abs(1-((X["z"] - z_min)/(z_max - z_min))) * (z_max - z_min)) + z_min
X["z"] = z_new
### convert pandas array into numpy array then into open3d object, plot and save
COORDINATES = X[["x", "y", "z"]]
COLOURS = X[["red", "green", "blue"]]/255
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(COORDINATES.to_numpy())
pcd.colors = o3d.utility.Vector3dVector(COLOURS.to_numpy())
o3d.visualization.draw_geometries([pcd], point_show_normal=True)
### plot
o3d.visualization.draw_geometries([pcd], point_show_normal=True)


data = read_ply("res/Lrigidum_seed_germination_propped_up.ply")
X = data['points'] ### extract datapoints as pandas array
### invert z orientation so that the tray isn't upsidedown by default
z_max = max(X["z"])
z_min = min(X["z"])
z_new = (abs(1-((X["z"] - z_min)/(z_max - z_min))) * (z_max - z_min)) + z_min
X["z"] = z_new
### convert pandas array into numpy array then into open3d object, plot and save
COORDINATES = X[["x", "y", "z"]]
COLOURS = X[["red", "green", "blue"]]/255
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(COORDINATES.to_numpy())
pcd.colors = o3d.utility.Vector3dVector(COLOURS.to_numpy())
o3d.visualization.draw_geometries([pcd], point_show_normal=True)
### plot
o3d.visualization.draw_geometries([pcd], point_show_normal=True)
