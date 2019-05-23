import math
import os
import numpy as np

def modele_creation(fichier_central, fichier_source):
    angle_degree = 3.6
    calibration = 0.4
    
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
    
    mon_fichier = open(fichier_central, "w")
    mon_fichier.write('')
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
        
        if i != (taille):
            mot = mot1 + ' ' + mot2 + ' ' + mot3 + '\n'
        else:
            mot = mot1 + ' ' + mot2 + ' ' + mot3
        mon_pcd.write(mot)
        
        i = i + 1

    mon_fichier = open(fichier_source, "r")
    contenu = mon_fichier.readlines()
    mon_fichier.close()
    
    taille = len(contenu)
    ''' if taille != 1:
        mon_pcd.write('\n') '''

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
        if(points[2] > -0.4  and points[2] < -0.35 and points[0] > -0.15 and points[0] < 0.15):
            test_point = calibration * math.tan(math.radians(3.8/10))
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
    
j = 0
fichier_source = ''
my_file = open("modele.pcd", "w")
my_file.write('')
my_file.close()
while j < 100:
    fichier_source = "test" + str(j) + ".pcd"
    modele_creation("modele.pcd",fichier_source)
    print(j)
    j = j + 1