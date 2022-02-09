#################
### Functions ###
#################

### import libraries
import os
import numpy as np
import pandas as pd
import open3d as o3d
import matplotlib.pyplot as plt
import random
from pyntcloud import PyntCloud

### Read ply file and output point cloud information (also inver the z-axis)
def fun_ply_read(fname, invert=False):
    ################################################
    ### TEST:
    # fname = "/home/jeff/Documents/plantSegment3D/res/Lr_test.ply"
    # X = fun_ply_read(fname)
    ################################################
    data = PyntCloud.from_file(fname)
    if (invert):
        data.points.z = -data.points.z
        # data.xyz[:,2] = -data.xyz[:,2]
        # data.centroid[2] = -data.centroid[2]
    return(data.points) ### ouput pandas array

### Save point cloud into a ply file
def fun_ply_save(pd_points, fname="ouput.ply"):
    ################################################
    ### TEST:
    # fname = "/home/jeff/Documents/plantSegment3D/res/Lr_test.ply"
    # pd_points = fun_ply_read(fname, invert=True)
    ################################################
    cloud = PyntCloud(
                pd.DataFrame(data=pd_points.to_numpy(),
                             columns=pd_points.axes[-1].to_numpy()
                            )
            )
    cloud.to_file(fname)
    return(0)

### plot 3D cloud models
def fun_ply_plot(pd_points, vec_coordinate_names=["x", "y", "z"], vec_colours=["red", "green", "blue"], colour_max_value=255):
    ################################################
    ### TEST
    # fname = "/home/jeffersonfparil/Downloads/data/Phenospex_scans/109_113-Glyphosate-ACC092_ACC091-REP2_1.ply"
    # pd_points = fun_ply_read(fname, invert=True)
    # fun_ply_save(pd_points)
    # vec_coordinate_names = ["x", "y", "z"]
    # vec_colours = ["red", "green", "blue"]
    # # vec_colours = ["ndvi"]
    # colour_max_value = 255
    # fun_ply_plot(pd_points, vec_colours=vec_colours)
    ################################################
    ### extract coordiantes
    mat_coordinates = pd_points[vec_coordinate_names].to_numpy()
    ### extract colours
    mat_colours = pd_points[vec_colours].to_numpy() / colour_max_value
    if mat_colours.shape[1] < 3:
        m = mat_colours.shape[0]
        n = 3 - mat_colours.shape[1]
        if mat_colours.shape[1] == 1:
            ### grayscale: copy the input channel to the other 2 channels
            # mat_replicates = np.repeat(mat_colours, n, axis=1)
            mat_replicates = np.repeat(mat_colours, n, axis=1)
            mat_replicates[:,0] = 1.0 - mat_colours.ravel()
            mat_replicates[:,1] = 0.0
            cmap = plt.get_cmap("viridis")
            colours = cmap(np.linspace(0,1,2**8))[:,0:3]
            mat_colours = colours[pd_points[vec_colours].to_numpy().ravel()]
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
    o3d.visualization.draw_geometries([pcd])




