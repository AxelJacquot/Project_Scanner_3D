import os
import numpy as np
import math

angle_degree = 90
# -0.25
# -0.3080-0.055
angle_radian = math.radians(angle_degree)

rotZ_Homo = np.array(  [[math.cos(angle_radian), 0  , math.sin(angle_radian),    0],
                        [0,                       1 ,     0,    0],
                        [-(math.sin(angle_radian)), 0,math.cos(angle_radian),    0],
                        [0,                       0,                          0,    1]])

mon_fichier = open("calib4.pcd", "r")

mon_pcd = open("calib5.pcd", "w")
mon_pcd.write('')
mon_pcd.close()

mon_pcd = open("calib5.pcd", "a")

contenu = mon_fichier.readlines()
taille = len(contenu)

for i in range(11):
    mon_pcd.write(contenu[i])
i = i + 1
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
    print(contenu_line_tmp)
    
    points = np.array([[float(contenu_line_tmp[0])],
                       [float(contenu_line_tmp[1])],
                       [float(contenu_line_tmp[2])],
                       [1]])
    
    pointsf = np.dot(rotZ_Homo, points)
    
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
    
    mon_pcd.write(mot)
    
    
    i = i + 1
    
mon_pcd.close()
mon_fichier.close()