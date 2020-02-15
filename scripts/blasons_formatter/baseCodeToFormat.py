import base64
from io import BytesIO
from PIL import Image

i = 0

with open('blasons.txt') as f:
        for line in f:
            nom = line.split(';')[0]
            b64 = line.split(';')[1]
            print(nom)
            im = Image.open(BytesIO(base64.b64decode(b64)))
            dir = "./images/"+str(i)+".png"
            im.save(dir, 'PNG')
            f = open("blasonsnames.txt", 'a')
            f.write(nom + '\n') 
            i = i + 1
f.closed


