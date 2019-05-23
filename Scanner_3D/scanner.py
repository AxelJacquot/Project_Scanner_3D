import math
import sys
import ctypes
import pyglet
import pyglet.gl as gl
import numpy as np
import pyrealsense2 as rs
import pcl
import os
import math
from open3d import *
import serial
from serial.tools.list_ports import comports

def ask_for_port():
    for n, (port, desc, hwid) in enumerate(sorted(comports()), 1):
        if desc == "FT232R USB UART":
            return port
    return 0

def ports():
    n = 0
    while n < 5:
        port = ask_for_port()
        if port == 0: 
            n = n + 1
            print("Veuillez brancher l'UART de la STM32")
            raw_input("Appuyer sur entree pour refaire une verification")
        else:
            return port
    print("FERMETURE DU PROGRAMME")   
    
ser = serial.Serial()
ser.baudrate = 115200
ser.port = ports()
ser.open()

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

# Configure streams
pipeline = rs.pipeline()
config = rs.config()

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

def capture_RealSense(name):
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

    ply = name + ".ply"
    pcd = name + ".pcd"
    points.export_to_ply(ply, color)
    clouding = pcl.load(ply)
    pcl.save(clouding, pcd)
    print("Export Reussi")
    
calibration = 0
 
def calibration_scanner():
    capture_RealSense("calibration")
    
    mon_fichier = open("calibration.pcd", "r")

    contenu = mon_fichier.readlines()
    taille = len(contenu)
    i = 11
    while i < taille:
        mot1 = ''
        mot2 = ''
        mot3 = ''
        mot = ''
        contenu_line_tmp = [0,0,0]
        test = ''
        
        test = contenu[i]
        taille_contenu = len(test)
        test = test.replace('\n','')
        contenu_line_tmp = test.split(" ")
        
        points = np.array([[float(contenu_line_tmp[0])],
                        [float(contenu_line_tmp[1])],
                        [float(contenu_line_tmp[2])]])
        
        if(points[1] < 1 and points[1] > 0.005 and points[2] > -0.4  and points[2] < -0.3 and points[0] > -0.15 and points[0] < 0.15):
            calibration = points[2]
        
        i = i + 1
        
    mon_fichier.close()
    
def modele_creation(fichier_central, fichier_source):
    angle_degree = 3.6
    
    angle_radian = math.radians(angle_degree)

    transZ = np.array(  [[0]  ,
                        [0]  ,
                        [calibration]]  )

    rotZ = np.array(   [[math.cos(angle_radian),    0, math.sin(angle_radian)],
                        [0                     ,    1, 0                     ],
                        [-(math.sin(angle_radian)), 0, math.cos(angle_radian)]]  )

    mon_fichier = open(fichier_central, "r")
    contenu = mon_fichier.readlines()
    mon_fichier.close()

    mon_pcd = open(fichier_central, "a")

    taille = len(contenu)

    i=0
    while i < taille:
        mot1 = ''
        mot2 = ''
        mot3 = ''
        mot = ''
        contenu_line_tmp = [0,0,0]
        test = ''
        
        test = contenu[i]
        taille_contenu = len(test)
        test = test.replace('\n','')
        contenu_line_tmp = test.split(" ")
        
        points = np.array([[float(contenu_line_tmp[0])],
                        [float(contenu_line_tmp[1])],
                        [float(contenu_line_tmp[2])]])
        
        pointsf = np.dot(rotZ, points)
        
        mot1 = str(pointsf[0])
        mot1 = mot1.replace('[','')
        mot1 = mot1.replace(']','')
        
        mot2 = str(pointsf[1])
        mot2 = mot2.replace('[','')
        mot2 = mot2.replace(']','')
        
        mot3 = str(pointsf[2])
        mot3 = mot3.replace('[','')
        mot3 = mot3.replace(']','')
        
        if i != (taille - 1):
            mot = mot1 + ' ' + mot2 + ' ' + mot3 + '\n'
        else:
            mot = mot1 + ' ' + mot2 + ' ' + mot3
        mon_pcd.write(mot)
        
        i = i + 1

    mon_fichier = open(fichier_source, "r")
    contenu = mon_fichier.readlines()
    mon_fichier.close()
    
    taille = len(contenu)
    
    mon_pcd.write('\n')

    i=11
    while i < taille:
        mot1 = ''
        mot2 = ''
        mot3 = ''
        mot = ''
        contenu_line_tmp = [0,0,0]
        test = ''
        
        test = contenu[i]
        taille_contenu = len(test)
        test = test.replace('\n','')
        contenu_line_tmp = test.split(" ")
        
        points = np.array([[float(contenu_line_tmp[0])],
                        [float(contenu_line_tmp[1])],
                        [float(contenu_line_tmp[2])]])
        if(points[1] < 1 and points[1] > 0.005 and points[2] > -0.4  and points[2] < -0.3 and points[0] > -0.15 and points[0] < 0.15):
            test_point = calibration * math.tan(math.radians(10))
            if (points[0] < test_point and points[0] > -test_point):
                
                pointsf = transZ + points
                
                mot1 = str(pointsf[0])
                mot1 = mot1.replace('[','')
                mot1 = mot1.replace(']','')
                
                mot2 = str(pointsf[1])
                mot2 = mot2.replace('[','')
                mot2 = mot2.replace(']','')
                
                mot3 = str(pointsf[2])
                mot3 = mot3.replace('[','')
                mot3 = mot3.replace(']','')
                
                
                if i != (taille - 1):
                    mot = mot1 + ' ' + mot2 + ' ' + mot3 + '\n'
                else:
                    mot = mot1 + ' ' + mot2 + ' ' + mot3
                mon_pcd.write(mot)
        
        i = i + 1
        
    mon_pcd.close()

def capture():
    i=0
    out = 0
    nom = raw_input("Nom du fichier de sortie: ")
    while i < 100:
        print("")
        nom2 = nom+("%d" % i)
        capture_RealSense(nom2)
        i = i+1
        data = 55
        ser.write([data])
        out = ser.read()
    return nom 

if __name__ == "__main__":
    while True:
        print("Menu des choix:")
        print("1- Calibration")
        print("2- Capture")
        print("3- Fabrication du modele complet")
        print("4- Conversion du fichier 3D")
        print("5- Visualisation du modele final")
        print("6- Quitter")
        choice = input("Faites votre choix: ")
        if choice == 1:
            pyglet.app.run()
            calibration_scanner()
            
        if choice == 2:
            nom5 = capture()
        if choice == 3:
            j = 0
            fichier_source = ''
            my_file = open("modele.pcd", "w")
            my_file.write('')
            my_file.close()
            while j < 100:
                fichier_source = nom5 + str(j) + ".pcd"
                modele_creation("modele.pcd",fichier_source)
                j = j + 1
        if choice == 4:
            print("Vous pouvez convertir votre fichier en:")
            print("obj")
            print("stl")
            print("ply")
            print("pcd")
            print("vtk")
            format_convert = raw_input("Format choisie: ")
            
            cmd = './pcl_converter ' + nom5 + '.pcd ' + nom5 + '.' + format_convert
            os.popen(cmd)
        if choice == 5:
            print("Visualisation modele finale")
        if choice == 6:
            os.remove('test_0.pcd')
            sys.exit(0)