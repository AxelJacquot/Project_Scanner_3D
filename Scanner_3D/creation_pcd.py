import os

i=0 

read_file = open("calib5.pcd", "r")
contenu = read_file.readlines()
points = len(contenu)
read_file.close()

file = open("test_pcd.pcd", "w")
file.write("")
file.close()

file = open("test_pcd.pcd", "a")
mot = ("# .PCD v0.7 - Point Cloud Data file format \n" +
       "FIELDS x y z\n" +
       "SIZE 4 4 4\n" +
       "TYPE F F F\n" +
       "COUNT 1 1 1\n" +
       "WIDTH " + str(points) + "\n" +
       "HEIGHT 1\n" +
       "VIEWPOINT 0 0 0 1 0 0 0\n" +
       "POINTS " + str(points) + "\n" +
       "DATA ascii\n")
file.write(mot)
while i < points:
    file.write(contenu[i])
    i = i + 1

file.close()
