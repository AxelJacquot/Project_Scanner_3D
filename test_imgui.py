import bimpy
import sys


i=0

a=0

vtk = bimpy.Bool(False)

stl = bimpy.Bool(False)

obj = bimpy.Bool(False)

ply = bimpy.Bool(False)

pcd = bimpy.Bool(False)

nom = bimpy.String()

atx

ctx = bimpy.Context()

ctx.init(800, 400, "Scanner 3D")

with ctx:
    bimpy.themes.set_light_theme()

taille_cible = bimpy.Int(150)

largeur_cible = bimpy.Int(150)

while not ctx.should_close():
    ctx.new_frame()

    bimpy.set_next_window_pos(bimpy.Vec2(0, 0), bimpy.Condition.Once)
    bimpy.set_next_window_size(bimpy.Vec2(800, 400), bimpy.Condition.Once)
    bimpy.begin("Controls")
    
    bimpy.input_text("Nom du fichier", nom, 15)

    if bimpy.button("Visualisation"):
        while(i < 1000000):
            num = i / 1000000
            bimpy.progress_bar(num)
            bimpy.end()
            ctx.render()
            i = i + 1
    if bimpy.button("Debut du Scan"):
        a = 2
    if bimpy.button("Visualisation du resultat"):
        a = 3
    bimpy.text("Choix des formats de sortie")
    
    bimpy.checkbox("VTK",vtk)
    
    bimpy.checkbox("STL",stl)
    
    bimpy.checkbox("OBJ",obj)

    bimpy.checkbox("PLY",ply)
    
    bimpy.checkbox("PCD",pcd)
    
    if bimpy.button("Conversion du fichier"):
        a=4
    
    if bimpy.button("Fermer l'application"):
        sys.exit(0)

    bimpy.end()

    ctx.render()
