#################
### Functions ###
#################

### import libraries
import os
import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt
import random
from pyntcloud import PyntCloud

### Read ply files and extract point cloud information
def fun_ply_read(fname):
    ################################################
    ### TEST:
    # os.chdir("/home/jeff/Documents/plantSegment3D/res")
    # fname = "Lr_test.ply"
    # X = fun_ply_read(fname)
    ################################################
    data = PyntCloud.from_file(fname)
    X = data.points
    return(X)

### plot 3D cloud models
def fun_ply_plo(X, vec_ccordinate_names=["x", "y", "z"], vec_colours=["red", "green", "blue"], colour_max_value=255):
    ################################################
    ### TEST
    # os.chdir("/home/jeff/Documents/plantSegment3D/res")
    # fname = "Lr_test.ply"
    # X = fun_ply_read(fname)
    # vec_ccordinate_names = ["x", "y", "z"]
    # vec_colours = ["red", "green", "blue"]
    # vec_colours = ["ndvi"]
    # colour_max_value = 255
    # fun_ply_plo(X, vec_colours=vec_colours)
    ################################################
    ### extract coordiantes
    mat_coordinates = X[vec_ccordinate_names].to_numpy()
    ### extract colours
    mat_colours = X[vec_colours].to_numpy() / colour_max_value
    if mat_colours.shape[1] < 3:
        m = mat_colours.shape[0]
        n = 3 - mat_colours.shape[1]
        if mat_colours.shape[1] == 1:
            ### grayscale: copy the input channel to the other 2 channels
            mat_replicates = np.repeat(mat_colours, n, axis=1)
        else:
            ### 2 colour channels, wth the input vectors in the red and green channels; while the blue channel is all zeros
            mat_replicates = np.zeros((m,n)) 
        mat_colours = np.concatenate((mat_colours, mat_replicates), axis=1)
    ### initialise a pointcloud object
    pcd = o3d.geometry.PointCloud()
    ### append the coordinates
    pcd.points = o3d.utility.Vector3dVector(mat_coordinates)
    pcd.colors = o3d.utility.Vector3dVector(mat_colours)
    ### plot
    o3d.visualization.draw_geometries([pcd], point_show_normal=True)
