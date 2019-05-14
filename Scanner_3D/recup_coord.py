import os
import numpy as np
import math

angle_degree = 25

angle_radian = math.radians(angle_degree)

rotY = np.array([[math.cos(angle_radian),0,math.sin(angle_radian)],
                  [0,1,0],
                  [-(math.sin(angle_radian)),0,math.cos(angle_radian)]])

mon_fichier = open("test0.pcd", "r")

mon_pcd = open("test_0.pcd", "a")

contenu = mon_fichier.readlines()
taille = len(contenu)

for i in range(11):
    print(contenu[i])
    mon_pcd.write(contenu[i])
i = i + 1
n = 0
while i < taille:
    mot1 = ''
    mot2 = ''
    mot3 = ''
    mot = ''
    contenu_line_tmp = [0,0,0]
    contenu_line = [0,0,0]
    test_tmp = ''
    test = ''
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
    
    mot1 = str(pointsf[0])
    mot1 = mot1.replace('[','')
    mot1 = mot1.replace(']','')
    
    mot2 = str(pointsf[1])
    mot2 = mot2.replace('[','')
    mot2 = mot2.replace(']','')
    
    mot3 = str(pointsf[2])
    mot3 = mot3.replace('[','')
    mot3 = mot3.replace(']','')
    
    mot = mot1 + ' ' + mot2 + ' ' + mot3 + '\n'
    
    print(mot)
    
    mon_pcd.write(mot)
    
    i = i + 1

mon_pcd.close()
mon_fichier.close()