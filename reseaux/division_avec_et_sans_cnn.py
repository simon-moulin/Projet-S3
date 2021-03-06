# -*- coding: utf-8 -*-
"""Division avec et sans CNN.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1eWO7Ri8HaVy7BHu_r9i9ODNs9hfYs5Ny
"""

# Commented out IPython magic to ensure Python compatibility.
#Importation librairies
import pathlib
import numpy as np
import os
import matplotlib.pyplot as plt
import random
import math
import cv2
import base64
from io import BytesIO
from PIL import Image
from tensorflow.keras.preprocessing.image import ImageDataGenerator
try:
  # %tensorflow_version only exists in Colab.
#   %tensorflow_version 2.x
except Exception:
  pass
import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers

print(tf.__version__)

#Importation du Google Drive
from google.colab import drive
drive.mount('/content/drive')

"""## Importation des images"""

import base64
from io import BytesIO
from PIL import Image

CATEGORIES = ["bend", "bend sinister", "chevron", "fess", "gyronny", "pale", "quarter", "saltire", "aucun"]
IMG_SIZE=50
descriptions = []
imgs = []
class_num = []

PATH_TO_DATA = 'drive/My Drive/blasons50_b64.txt'

def isole_categorie(desc) :
    desc = desc.replace(',','').replace('imperial','')
    desc = desc.split(' ')

    if "gyronny" in desc:
        return "gyronny"

    if "quarterly" in desc:
        return "quarter"

    if "per" in desc:
        if "sinister" in desc:
            return "bend sinister"
       
        index_per = desc.index("per")
        return desc[index_per+1]
    else :
        return "aucun"
        
with open(PATH_TO_DATA) as f:
    for line in f:
        # on prend la description entière
        description_line = line.split(';')[0]

        # on prend l'image
        b64 = line.split(';')[1]
        img = Image.open(BytesIO(base64.b64decode(b64)))
        img_array = np.array(img)
        #resize array
        #new_array=cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
        imgs.append(img_array)

        categorie = isole_categorie(description_line)
        class_num.append(CATEGORIES.index(categorie))
        descriptions.append(categorie)


# Resize array, keras préfere
descriptions = np.array(descriptions).reshape((-1, 1))
imgs = np.array(imgs).reshape(-1, IMG_SIZE, IMG_SIZE, 4)
class_num = np.array(class_num).reshape((-1, 1))

plt.imshow(imgs[4])
print(descriptions[4])

# Pour l'entrainement

nombre_donnees = round(len(imgs),-1)

nombre_donnees_apprentissage = int(round(nombre_donnees*0.75,-1))
print(type(nombre_donnees_apprentissage))

X = imgs[:nombre_donnees_apprentissage]
y = class_num[:nombre_donnees_apprentissage]

plt.imshow(imgs[0])
print(CATEGORIES[class_num[0][0]])

# Pour les test
X_test = imgs[nombre_donnees_apprentissage:nombre_donnees]
y_test = class_num[nombre_donnees_apprentissage:nombre_donnees]

# Print----------------------------
print (len(X))
print (len(y))

"""## Avec CNN"""

#Création du modèle
model1 = tf.keras.Sequential([
    tf.keras.layers.Conv2D(4, (3,3), padding='same', activation=tf.nn.relu,
                           input_shape=(IMG_SIZE, IMG_SIZE, 4)),
    tf.keras.layers.MaxPooling2D((2, 2), strides=2),
    tf.keras.layers.Conv2D(8, (3,3), padding='same', activation=tf.nn.relu),
    tf.keras.layers.MaxPooling2D((2, 2), strides=2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(64, activation=tf.nn.relu),
    tf.keras.layers.Dense(64, activation=tf.nn.relu),
    tf.keras.layers.Dense(len(CATEGORIES),  activation=tf.nn.softmax)
])

model1.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

datagen = ImageDataGenerator(
      rescale=1.3/255,
      rotation_range=10,
      zoom_range=0.2,
      brightness_range=(0.3, 1.0),
      width_shift_range=0.1,
      fill_mode='constant',
      cval=255)

image_iterator = datagen.flow(X, batch_size=10)

for i in range (0,10):
    plt.imshow(image_iterator.next()[i])
    plt.show()
#Entrainement
model1.fit_generator(
        datagen.flow(X, y,batch_size=1),
        epochs=6)

model1.save('divisionCNNSayian.h5')

"""## Sans CNN"""

model2 = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=(IMG_SIZE, IMG_SIZE, 4)),
    tf.keras.layers.Dense(64, activation=tf.nn.relu),
    tf.keras.layers.Dense(64, activation=tf.nn.relu),
    tf.keras.layers.Dense(len(CATEGORIES),  activation=tf.nn.softmax)
])

model2.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

datagen = ImageDataGenerator(
      rescale=1.3/255,
      rotation_range=10,
      zoom_range=0.2,
      brightness_range=(0.3, 1.0),
      width_shift_range=0.1,
      fill_mode='constant',
      cval=255)

#Entrainement
model2.fit_generator(
        datagen.flow(X, y),
        epochs=6)

"""## Validation et prédictions"""

test_loss, test_accuracy = model1.evaluate(X_test, y_test)
print('Accuracy on test dataset:', test_accuracy)

test_loss, test_accuracy = model2.evaluate(X_test, y_test)
print('Accuracy on test dataset:', test_accuracy)

#Changer l'indice pour predire dans les arrays X_test et y_test
a = random.randint(0,len(X_test))

img = X_test[a]
plt.imshow(img)
img = np.array([img],dtype="float16")
print(CATEGORIES[y_test[a][0]])

predictions = model1.predict(img)
print(CATEGORIES[np.argmax(predictions[0])])

photo = Image.open("drive/My Drive/photo/14.jpg")
photo = photo.resize((50, 50))

photo = np.array(photo)
photo = np.concatenate(([photo, 255 * np.ones((50, 50, 1), dtype=np.uint8)]), axis=-1)

print(photo.shape)
plt.imshow(photo)

img = np.array([photo],dtype="float16")


result = []

predictions = model1.predict(img)
print(predictions[0])
result.append(np.argmax(predictions[0]))

DIVISIONS = ["bend", "bend sinister", "chevron", "fess", "gyronny", "pale", "quarter", "saltire", "aucun"]

print(result[0])

img_trans = datagen.random_transform(X_test[0])
plt.imshow(img_trans)