import os
import numpy as np
import math

mon_fichier = open("test0.pcd", "r")

mon_pcd = open("test_0.pcd", "w")
mon_pcd.write('')
mon_pcd.close()

mon_pcd = open("test_0.pcd", "a")

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
    
    points = np.array([[float(contenu_line_tmp[0])],
                       [float(contenu_line_tmp[1])],
                       [float(contenu_line_tmp[2])]])
    
    if(points[2] > -0.5  and points[2] < -0.32 and points[0] > -0.25 and points[0] < 0.25):
        test_point = -points[2] * math.tan(math.radians(3.6))
        if (points[0] < test_point and points[0] > -test_point):
            mot1 = str(points[0])
            mot1 = mot1.replace('[','')
            mot1 = mot1.replace(']','')
            
            mot2 = str(points[1])
            mot2 = mot2.replace('[','')
            mot2 = mot2.replace(']','')
            
            mot3 = str(points[2])
            mot3 = mot3.replace('[','')
            mot3 = mot3.replace(']','')
            
            mot = mot1 + ' ' + mot2 + ' ' + mot3 + '\n'
            
            mon_pcd.write(mot)
    
    
    i = i + 1
    
mon_pcd.close()
mon_fichier.close()