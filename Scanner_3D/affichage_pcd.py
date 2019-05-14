import pcl
from open3d import *
import numpy as np

voxel_size = 0.02


def load_point_clouds(voxel_size = 0.0):
    pcds = []
    pcd = read_point_cloud("test_0.pcd")
    pcd_down = voxel_down_sample(pcd, voxel_size = voxel_size)
    pcds.append(pcd_down)
    return pcds

if __name__ == "__main__":

    pcds_down = load_point_clouds(voxel_size)
    draw_geometries(pcds_down)