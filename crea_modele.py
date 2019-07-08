import math
import os
import numpy as np

modele = []
angle_degree = 3.6
calibration = 0.345

def modele_creation(fichier_source):
    
    angle_radian = math.radians(angle_degree)

    transZ = np.array(  [[0]  ,
                        [0]  ,
                        [calibration]]  )

    rotZ = np.array(   [[math.cos(angle_radian),    0, math.sin(angle_radian)],
                        [0                     ,    1, 0                     ],
                        [-(math.sin(angle_radian)), 0, math.cos(angle_radian)]]  )
    
    taille = len(modele)

    i=0
    
    while i < taille:
        contenu_line_tmp = [0,0,0]
        test = ''
        
        test = modele[i]
        
        pointsf = np.dot(rotZ, test)
        
        modele[i] = pointsf
        
        i = i + 1

    mon_fichier = open(fichier_source, "r")
    contenu = mon_fichier.readlines()
    mon_fichier.close()
    
    taille = len(contenu)

    i=11
    while i < taille:
        contenu_line_tmp = [0,0,0]
        test = ''
        
        test = contenu[i]
        test = test.replace('\n','')
        contenu_line_tmp = test.split(" ")
        
        points = np.array([[float(contenu_line_tmp[0])],
                        [float(contenu_line_tmp[1])],
                        [float(contenu_line_tmp[2])]])
        if(points[1] < 0.1 and points[1] > -0.075 and points[2] > -0.5  and points[2] < -0.2 and points[0] > -0.15 and points[0] < 0.15):
            test_point = calibration * math.tan(math.radians(3.6/10))
            if (points[0] < test_point and points[0] > -test_point):
                
                pointsf = transZ + points
                
                modele.append(pointsf)


        i = i + 1
    
j = 0
fichier_source = ''
my_file = open("test.pcd", "w")
my_file.write('')
my_file.close()
while j < 100:
    fichier_source = "aa" + str(j) + ".pcd"
    modele_creation(fichier_source)
    print(j)
    j = j + 1
my_file = open("test.pcd", "a")
i = 0
taille = len(modele)
mot = ("# .PCD v0.7 - Point Cloud Data file format \n" +
           "FIELDS x y z\n" +
           "SIZE 4 4 4\n" +
           "TYPE F F F\n" +
           "COUNT 1 1 1\n" +
           "WIDTH " + str(taille) + "\n" +
           "HEIGHT 1\n" +
           "VIEWPOINT 0 0 0 1 0 0 0\n" +
           "POINTS " + str(taille) + "\n" +
           "DATA ascii\n")
my_file.write(mot)

while i < taille:
    pointsf = modele[i]
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
        
    my_file.write(mot)
    
    i = i + 1
my_file.close()