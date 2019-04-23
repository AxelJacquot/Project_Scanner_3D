import math
import ctypes
import pyglet
import pyglet.gl as gl
import numpy as np
import pyrealsense2 as rs
import pcl
from open3d import *

class AppState:
    def __init__(self, *args, **kwargs):
        self.pitch, self.yaw = math.radians(-10), math.radians(-15)
        self.translation = np.array([0, 0, 1], np.float32)
        self.distance = 2
        self.mouse_btns = [False, False, False]
        self.paused = False
        self.decimate = 0
        self.color = True
        self.postprocessing = True

    def reset(self):
        self.pitch, self.yaw, self.distance = 0, 0, 2
        self.translation[:] = 0, 0, 1

state = AppState()

#Multiway_Registration Init
voxel_size = 0.02
max_correspondence_distance_coarse = voxel_size * 15
max_correspondence_distance_fine = voxel_size * 1.5

# Configure streams
pipeline = rs.pipeline()
config = rs.config()
print("Veuillez choisir une resolution parmi les suivantes")
print("1: 240p")
print("2: 480p")
print("3: 720p")
resol = input()
if resol == 1:
    config.enable_stream(rs.stream.depth, 320, 240, rs.format.z16, 30)
    #other_stream, other_format = rs.stream.infrared, rs.format.y8
    other_stream, other_format = rs.stream.color, rs.format.rgb8
    config.enable_stream(other_stream, 320, 240, other_format, 30)
elif resol == 2:
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    #other_stream, other_format = rs.stream.infrared, rs.format.y8
    other_stream, other_format = rs.stream.color, rs.format.rgb8
    config.enable_stream(other_stream, 640, 480, other_format, 30)
elif resol == 3:
    config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
    #other_stream, other_format = rs.stream.infrared, rs.format.y8
    other_stream, other_format = rs.stream.color, rs.format.rgb8
    config.enable_stream(other_stream, 1280, 720, other_format, 30)

# Start streaming
pipeline.start(config)
profile = pipeline.get_active_profile()

depth_sensor = profile.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()

depth_profile = rs.video_stream_profile(profile.get_stream(rs.stream.depth))
depth_intrinsics = depth_profile.get_intrinsics()
w, h = depth_intrinsics.width, depth_intrinsics.height

# Processing blocks
pc = rs.pointcloud()
decimate = rs.decimation_filter()
decimate.set_option(rs.option.filter_magnitude, 2 ** state.decimate)
colorizer = rs.colorizer()
filters = [rs.disparity_transform(),
           rs.spatial_filter(),
           rs.temporal_filter(),
           rs.disparity_transform(False)]

# pyglet
window = pyglet.window.Window(
    config=gl.Config(
        double_buffer=True,
        samples=16  # MSAA
    ),
    resizable=True, vsync=True)
keys = pyglet.window.key.KeyStateHandler()
window.push_handlers(keys)

def convert_fmt(fmt):
    """rs.format to pyglet format string"""
    return {
        rs.format.rgb8: 'RGB',
        rs.format.bgr8: 'BGR',
        rs.format.rgba8: 'RGBA',
        rs.format.bgra8: 'BGRA',
        rs.format.y8: 'L',
    }[fmt]

# Create a VertexList to hold pointcloud data
# Will pre-allocates memory according to the attributes below
vertex_list = pyglet.graphics.vertex_list(
    w * h, 'v3f/stream', 't2f/stream', 'n3f/stream')
# Create and allocate memory for our color data
other_profile = rs.video_stream_profile(profile.get_stream(other_stream))
image_data = pyglet.image.ImageData(w, h, convert_fmt(
    other_profile.format()), (gl.GLubyte * (w * h * 3))())

#fps_display = pyglet.clock.ClockDisplay()

@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    w, h = map(float, window.get_size())

    if buttons & pyglet.window.mouse.LEFT:
        state.yaw -= dx * 0.5
        state.pitch -= dy * 0.5

    if buttons & pyglet.window.mouse.RIGHT:
        dp = np.array((dx / w, -dy / h, 0), np.float32)
        state.translation += np.dot(state.rotation, dp)

    if buttons & pyglet.window.mouse.MIDDLE:
        dz = dy * 0.01
        state.translation -= (0, 0, dz)
        state.distance -= dz

def handle_mouse_btns(x, y, button, modifiers):
    state.mouse_btns[0] ^= (button & pyglet.window.mouse.LEFT)
    state.mouse_btns[1] ^= (button & pyglet.window.mouse.RIGHT)
    state.mouse_btns[2] ^= (button & pyglet.window.mouse.MIDDLE)

window.on_mouse_press = window.on_mouse_release = handle_mouse_btns

@window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    dz = scroll_y * 0.1
    state.translation -= (0, 0, dz)
    state.distance -= dz

def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.R:
        state.reset()

    if symbol == pyglet.window.key.P:
        state.paused ^= True

    if symbol == pyglet.window.key.D:
        state.decimate = (state.decimate + 1) % 3
        decimate.set_option(rs.option.filter_magnitude, 2 ** state.decimate)

    if symbol == pyglet.window.key.C:
        state.color ^= True

    if symbol == pyglet.window.key.F:
        state.postprocessing ^= True

    if symbol == pyglet.window.key.S:
        pyglet.image.get_buffer_manager().get_color_buffer().save('out.png')
    
    if symbol == pyglet.window.key.A:
        pyglet.image.get_buffer_manager().get_depth_buffer().save('out.png')

    if symbol == pyglet.window.key.Q:
        window.close()

window.push_handlers(on_key_press)

@window.event
def on_draw():
    window.clear()

    gl.glEnable(gl.GL_DEPTH_TEST)
    gl.glEnable(gl.GL_LINE_SMOOTH)

    width, height = window.get_size()
    gl.glViewport(0, 0, width, height)

    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadIdentity()
    gl.gluPerspective(60, width / float(height), 0.01, 20)

    gl.glMatrixMode(gl.GL_TEXTURE)
    gl.glLoadIdentity()
    # texcoords are [0..1] and relative to top-left pixel corner, add 0.5 to center
    gl.glTranslatef(0.5 / image_data.width, 0.5 / image_data.height, 0)
    # texture size may be increased by pyglet to a power of 2
    tw, th = image_data.texture.owner.width, image_data.texture.owner.height
    gl.glScalef(image_data.width / float(tw),
                image_data.height / float(th), 1)

    gl.glMatrixMode(gl.GL_MODELVIEW)
    gl.glLoadIdentity()

    gl.gluLookAt(0, 0, 0, 0, 0, 1, 0, -1, 0)

    gl.glTranslatef(0, 0, state.distance)
    gl.glRotated(state.pitch, 1, 0, 0)
    gl.glRotated(state.yaw, 0, 1, 0)

    """ if any(state.mouse_btns):
        axes(0.1, 4) """

    gl.glTranslatef(0, 0, -state.distance)
    gl.glTranslatef(*state.translation)

    gl.glColor3f(0.5, 0.5, 0.5)
    gl.glPushMatrix()
    gl.glTranslatef(0, 0.5, 0.5)
    #grid()
    gl.glPopMatrix()

    psz = 1
    gl.glPointSize(psz)
    distance = (1, 0, 0)
    gl.glPointParameterfv(gl.GL_POINT_DISTANCE_ATTENUATION,
                          (gl.GLfloat * 3)(*distance))

    gl.glColor3f(1, 1, 1)
    texture = image_data.get_texture()
    gl.glEnable(texture.target)
    gl.glBindTexture(texture.target, texture.id)
    gl.glTexParameteri(
        gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)

    # comment this to get round points with MSAA on
    gl.glEnable(gl.GL_POINT_SPRITE)
    
    gl.glDisable(gl.GL_MULTISAMPLE)  # for true 1px points with MSAA on
    vertex_list.draw(gl.GL_POINTS)
    gl.glDisable(texture.target)
    gl.glEnable(gl.GL_MULTISAMPLE)

    gl.glDisable(gl.GL_LIGHTING)

    gl.glColor3f(0.25, 0.25, 0.25)
    #frustum(depth_intrinsics)
    #axes()

    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadIdentity()
    gl.glOrtho(0, width, 0, height, -1, 1)
    gl.glMatrixMode(gl.GL_MODELVIEW)
    gl.glLoadIdentity()
    gl.glMatrixMode(gl.GL_TEXTURE)
    gl.glLoadIdentity()
    gl.glDisable(gl.GL_DEPTH_TEST)

    #fps_display.draw()

def run(dt):
    points = rs.points()
    global w, h
    window.set_caption("RealSense (%dx%d) %dFPS (%.2fms) %s" %
                       (w, h, 0 if dt == 0 else 1.0 / dt, dt * 1000,
                        "PAUSED" if state.paused else ""))

    if state.paused:
        return

    success, frames = pipeline.try_wait_for_frames(timeout_ms=0)
    if not success:
        return

    depth_frame = frames.get_depth_frame()
    other_frame = frames.first(other_stream)
    color = frames.get_color_frame()

    depth_frame = decimate.process(depth_frame)

    if state.postprocessing:
        for f in filters:
            depth_frame = f.process(depth_frame)

    # Grab new intrinsics (may be changed by decimation)
    depth_intrinsics = rs.video_stream_profile(
        depth_frame.profile).get_intrinsics()
    w, h = depth_intrinsics.width, depth_intrinsics.height

    color_image = np.asanyarray(other_frame.get_data())

    colorized_depth = colorizer.colorize(depth_frame)
    depth_colormap = np.asanyarray(colorized_depth.get_data())

    if state.color:
        mapped_frame, color_source = other_frame, color_image
    else:
        mapped_frame, color_source = colorized_depth, depth_colormap

    points = pc.calculate(depth_frame)

    pc.map_to(mapped_frame)

    if keys[pyglet.window.key.E]:
        #points.export_to_ply("out.ply", color_source)
        points.export_to_ply("out.ply", color)
        clouding = pcl.load("out.ply")
        pcl.save(clouding, "out.pcd")
        print("Export Reussi")

    pc.map_to(mapped_frame)

    # handle color source or size change
    fmt = convert_fmt(mapped_frame.profile.format())
    global image_data
    if (image_data.format, image_data.pitch) != (fmt, color_source.strides[0]):
        empty = (gl.GLubyte * (w * h * 3))()
        image_data = pyglet.image.ImageData(w, h, fmt, empty)
    # copy image deta to pyglet
    image_data.set_data(fmt, color_source.strides[0], color_source.ctypes.data)

    verts = np.asarray(points.get_vertices(2)).reshape(h, w, 3)
    texcoords = np.asarray(points.get_texture_coordinates(2))

    if len(vertex_list.vertices) != verts.size:
        vertex_list.resize(verts.size // 3)
        # need to reassign after resizing
        vertex_list.vertices = verts.ravel()
        vertex_list.tex_coords = texcoords.ravel()

    copy(vertex_list.vertices, verts)
    copy(vertex_list.tex_coords, texcoords)

# copy our data to pre-allocated buffers, this is faster than assigning...
# pyglet will take care of uploading to GPU
def copy(dst, src):
    """copy numpy array to pyglet array"""
    # timeit was mostly inconclusive, favoring slice assignment for safety
    np.array(dst, copy=False)[:] = src.ravel()
    # ctypes.memmove(dst, src.ctypes.data, src.nbytes)

pyglet.clock.schedule(run)

def load_point_clouds(name, voxel_size = 0.0):
    pcds = []
    for i in range(10):
        nom = name + ("%d" % i) + (".pcd")
        pcd = read_point_cloud(name)
        pcd_down = voxel_down_sample(pcd, voxel_size = voxel_size)
        pcds.append(pcd_down)
    return pcds


def pairwise_registration(source, target):
    print("Apply point-to-plane ICP")
    icp_coarse = registration_icp(source, target,
            max_correspondence_distance_coarse, np.identity(4),
            TransformationEstimationPointToPlane())
    icp_fine = registration_icp(source, target,
            max_correspondence_distance_fine, icp_coarse.transformation,
            TransformationEstimationPointToPlane())
    transformation_icp = icp_fine.transformation
    information_icp = get_information_matrix_from_point_clouds(
            source, target, max_correspondence_distance_fine,
            icp_fine.transformation)
    return transformation_icp, information_icp


def full_registration(pcds,
        max_correspondence_distance_coarse, max_correspondence_distance_fine):
    pose_graph = PoseGraph()
    odometry = np.identity(4)
    pose_graph.nodes.append(PoseGraphNode(odometry))
    n_pcds = len(pcds)
    for source_id in range(n_pcds):
        for target_id in range(source_id + 1, n_pcds):
            transformation_icp, information_icp = pairwise_registration(
                    pcds[source_id], pcds[target_id])
            print("Build PoseGraph")
            if target_id == source_id + 1: # odometry case
                odometry = np.dot(transformation_icp, odometry)
                pose_graph.nodes.append(PoseGraphNode(np.linalg.inv(odometry)))
                pose_graph.edges.append(PoseGraphEdge(source_id, target_id,
                        transformation_icp, information_icp, uncertain = False))
            else: # loop closure case
                pose_graph.edges.append(PoseGraphEdge(source_id, target_id,
                        transformation_icp, information_icp, uncertain = True))
    return pose_graph

def capture(name):
    points = rs.points()

    success, frames = pipeline.try_wait_for_frames(timeout_ms=10)

    depth_frame = frames.get_depth_frame()
    other_frame = frames.first(other_stream)
    color = frames.get_color_frame()

    depth_frame = decimate.process(depth_frame)

    if state.postprocessing:
        for f in filters:
            depth_frame = f.process(depth_frame)

    points = pc.calculate(depth_frame)

    pc.map_to(other_frame)

    #points.export_to_ply("out.ply", color_source)
    ply = name + ".ply"
    pcd = name + ".pcd"
    points.export_to_ply(ply, color)
    clouding = pcl.load(ply)
    pcl.save(clouding, pcd)
    print("Export Reussi")
    # handle color source or size change
    #fmt = convert_fmt(mapped_frame.profile.format())

if __name__ == "__main__":
    while 1:
        print("Menu des choix:")
        print("1- Visualisation")
        print("2- Capture")
        print("3- Fabrication du modele complet")
        tes = input("Faites votre choix: ")
        if tes == 1:
            pyglet.app.run()
        if tes ==2:
            i=0
            nom = input("Nom du fichier de sortie: ")
            while i < 10:
                print("")
                nom2 = nom+("%d" % i)
                capture(nom2)
                i = i+1
        if tes == 3:
            nom = input("Nom du fichier de sortie: ")
            set_verbosity_level(VerbosityLevel.Debug)
            pcds_down = load_point_clouds(nom, voxel_size)
            draw_geometries(pcds_down)

            print("Full registration ...")
            pose_graph = full_registration(pcds_down,
                    max_correspondence_distance_coarse,
                    max_correspondence_distance_fine)

            print("Optimizing PoseGraph ...")
            option = GlobalOptimizationOption(
                    max_correspondence_distance = max_correspondence_distance_fine,
                    edge_prune_threshold = 0.25,
                    reference_node = 0)
            global_optimization(pose_graph,
                    GlobalOptimizationLevenbergMarquardt(),
                    GlobalOptimizationConvergenceCriteria(), option)

            print("Transform points and display")
            for point_id in range(len(pcds_down)):
                print(pose_graph.nodes[point_id].pose)
                pcds_down[point_id].transform(pose_graph.nodes[point_id].pose)
            draw_geometries(pcds_down)

            print("Make a combined point cloud")
            pcds = load_point_clouds(voxel_size)
            pcd_combined = PointCloud()
            for point_id in range(len(pcds)):
                pcds[point_id].transform(pose_graph.nodes[point_id].pose)
                pcd_combined += pcds[point_id]
            pcd_combined_down = voxel_down_sample(pcd_combined, voxel_size = voxel_size)
            write_point_cloud("multiway_registration.pcd", pcd_combined_down)
            draw_geometries([pcd_combined_down])