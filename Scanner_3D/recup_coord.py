import os
import numpy as np

mot1 = ''
mot2 = ''
mot3 = ''



mon_fichier = open("test0.pcd", "r")
contenu = mon_fichier.readlines()
taille = len(contenu)

for i in range(11):
    print(contenu[i])
i = i + 1
n = 0
while i < taille:
    contenu_line = [0,0,0]
    test_tmp = ''
    test = contenu[i]
    taille_contenu = len(test)
    for j in range(taille_contenu):
        if test[j] != '\n':
            test_tmp = test_tmp + test[j]
    contenu_line = test_tmp.split(" ")
                
    print(contenu_line)
   
    i = i + 1

mon_fichier.close()