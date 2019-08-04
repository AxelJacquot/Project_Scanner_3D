from __future__ import absolute_import, print_function
import pyopencl as cl
import numpy as np
from time import time
from math import pi


a = np.random.rand(999999).astype(np.float32).reshape(333333,3)

"""a = np.array(
    [[0.54543, 0.1545, 0.78430], [0.2454, 0.45484, 1.25780], [0.2454, 0.45484, 1.25780], [0.56415, 0.845161, 0.5488199],
     [0.2454, 0.45484, 0.1216], [0.2454, 0.45484, 1.25780], [0.62147, 0.03146, 0.79410], [0., 0., 0.],
     [0.2454, 0.45484, 1.25780], [0., 0.2, 0.]]).astype(np.float32)
"""

angle = 180 * pi/180

ctx = cl.create_some_context(None,[0])
queue = cl.CommandQueue(ctx)

mf = cl.mem_flags
a_g = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=a)
angle_g = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=np.float32(angle))
# b_g = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=b)
# c_g = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=b)static

prg = cl.Program(ctx, """
__kernel void traitement(__global const float *point, __global float *point_prime)
{
    int i = (get_global_id(0) * 2) + get_global_id(0);
    if(point[i] < 0.5 && point[i] > -0.5){
        if(point[i+1] < 0.5 && point[i+1] > -0.5){
            if(point[i+2] < 0.5 && point[i+2] > -0.5){
                point_prime[i] = point[i];
                point_prime[i+1] = point[i+1];
                point_prime[i+2] = point[i+2];
            }
        }
    }
    
}
__kernel void rot_x(__global const float *point, __global float *angle, __global float *point_prime)
{
    float angle_x = *angle;
    int i = (get_global_id(0) * 2) + get_global_id(0);
    point_prime[i] = point[i];
    point_prime[i+1] = cos(angle_x) * point[i+1] + sin(angle_x) * point[i+2];
    point_prime[i+2] = cos(angle_x) * point[i+2] - sin(angle_x) * point[i+1];
}

__kernel void rot_y(__global const float *point, __global float *angle, __global float *point_prime)
{
    float angle_y = *angle;
    int i = (get_global_id(0) * 2) + get_global_id(0);
    point_prime[i] = cos(angle_y) * point[i] - sin(angle_y) * point[i+2];
    point_prime[i+1] = point[i+1];
    point_prime[i+2] = cos(angle_y) * point[i+2] + sin(angle_y) * point[i];
}

__kernel void rot_z(__global const float *point, __global float *angle, __global float *point_prime)
{
    float angle_z = *angle;
    int i = (get_global_id(0) * 2) + get_global_id(0);
    point_prime[i] = cos(angle_z) * point[i] + sin(angle_z) * point[i+1];
    point_prime[i+1] = cos(angle_z) * point[i+1] - sin(angle_z) * point[i];
    point_prime[i+2] = point[i+2];
}
""").build()

tr_g = cl.Buffer(ctx, mf.WRITE_ONLY, a.nbytes)

starttime = time()
prg.traitement(queue, a.shape, None, a_g, tr_g)
tr_np = np.empty_like(a)
cl.enqueue_copy(queue, tr_np, tr_g)

a = tr_np[~np.all(tr_np == 0., axis=1)]         #delete all occurence of [0 0 0]

a_g = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=a)
res_g = cl.Buffer(ctx, mf.WRITE_ONLY, a.nbytes)
x_g = cl.Buffer(ctx, mf.WRITE_ONLY, a.nbytes)
y_g = cl.Buffer(ctx, mf.WRITE_ONLY, a.nbytes)
prg.rot_z(queue, a.shape, None, a_g, angle_g, res_g)
prg.rot_x(queue, a.shape, None, res_g, angle_g, x_g)
prg.rot_y(queue, a.shape, None, x_g, angle_g, y_g)

res_np = np.empty_like(a)
x_np = np.empty_like(a)
y_np = np.empty_like(a)
cl.enqueue_copy(queue, res_np, res_g)
cl.enqueue_copy(queue, x_np, x_g)
cl.enqueue_copy(queue, y_np, y_g)

# Check on CPU with Numpy:
print(time() - starttime)
print(a)
print(res_np)
print(x_np)
print(y_np)
print(a.shape[0])
