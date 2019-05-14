import os
import numpy as np
import math

mot1 = ''
mot2 = ''
mot3 = ''


angle_degree = 25

angle_radian = math.radians(angle_degree)

rotY = np.array([[math.cos(angle_radian),0,math.sin(angle_radian)],
                  [0,1,0],
                  [-(math.sin(angle_radian)),0,math.cos(angle_radian)]])

mon_fichier = open("test0.pcd", "r")
contenu = mon_fichier.readlines()
taille = len(contenu)

for i in range(11):
    print(contenu[i])
i = i + 1
n = 0
while i < taille:
    contenu_line_tmp = [0,0,0]
    contenu_line = [0,0,0]
    test_tmp = ''
    test = contenu[i]
    taille_contenu = len(test)
    for j in range(taille_contenu):
        if test[j] != '\n':
            test_tmp = test_tmp + test[j]
    contenu_line_tmp = test_tmp.split(" ")
    
    points = np.array([[float(contenu_line_tmp[0])],
                       [float(contenu_line_tmp[1])],
                       [float(contenu_line_tmp[2])]])
    
    pointsf = np.dot(rotY, points)
                
    print(pointsf)
   
    i = i + 1

mon_fichier.close()