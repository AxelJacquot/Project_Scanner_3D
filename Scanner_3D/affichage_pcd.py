import pcl
from open3d import *
import numpy as np

voxel_size = 0.0001


def load_point_clouds(voxel_size = 0.0):
    pcd = read_point_cloud("calib5.pcd")
    return [pcd]

if __name__ == "__main__":

    pcds_down = load_point_clouds(voxel_size)
    draw_geometries(pcds_down)