import base64
from io import BytesIO
from PIL import Image
import os

i = 0
os.mkdir("argent")
os.mkdir("azure")
os.mkdir("gules")
os.mkdir("or")
os.mkdir("purpure")
os.mkdir("sable")
os.mkdir("vert")

with open('blasons.txt') as f:
    for line in f:
        couleur = line.split(' ')[0]
        couleur = couleur.split(',')[0] #Removing the ',' 
        print(couleur)
        b64 = line.split(';')[1]
        im = Image.open(BytesIO(base64.b64decode(b64)))
        dir = "./" + couleur + "/"+str(i)+".png"
        im.save(dir, 'PNG')
        i = i + 1
f.closed


