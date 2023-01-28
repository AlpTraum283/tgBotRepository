from PIL import Image
from PIL import ImageFilter
from PIL import ImageEnhance
import numpy as np
import cv2
import matplotlib.pyplot as plt
import os

buttonNameList = ['Поворот', 'Размытие', 'Чёрно-белое', 'Применить маску', 'Закончить обработку']

buttonNameDegreeList = ['90° влево', '90° вправо']

buttonIdDegreeList = ['90', '270']

buttonFilterNameList = ['Маска кошки', 'Маска собаки', 'Маска лисы']

subButtonList = ['Подписаться', 'Позже'] 



def imageRotateLeft(fileName, chat_ID, degree):
    changed_image_name = ('changed_' + str(chat_ID) + '.jpg')
    image = Image.open(fileName)
    rotated_image = image.rotate(degree, expand = True)
    rotated_image.save(changed_image_name, quality = 100)
    return str(changed_image_name)

def imageBlurFilter(fileName, chat_ID):
    changed_image_name = ('changed_' + str(chat_ID) + '.jpg')
    image = Image.open(fileName)
    blured_image = image.filter(ImageFilter.BLUR)
    blured_image.save(changed_image_name, quality = 100)
    return str(changed_image_name)

def imageContourFilter(fileName, chat_ID):
    changed_image_name = ('changed_' + str(chat_ID) + '.jpg')
    image = Image.open(fileName)
    contoured_image = image.filter(ImageFilter.CONTOUR)
    contoured_image.save(changed_image_name, quality = 100)
    return str(changed_image_name)

def imageBWFilter(fileName, chat_ID):
    changed_image_name = ('changed_' + str(chat_ID) + '.jpg')
    image = Image.open(fileName)
    enhanceImage = ImageEnhance.Color(image)
    BW_image = enhanceImage.enhance(0.0)
    BW_image.save(changed_image_name, quality = 100)
    return str(changed_image_name)


def drawCatMask(img, chat_ID):
    changed_image_name = ('changed_' + str(chat_ID) + '.jpg')
    image = Image.open(img)
    imageFilter = Image.open('catFilter.png')

    test_image = cv2.imread(img)
    image_copy = test_image.copy()
    test_image_gray = cv2.cvtColor(image_copy, cv2.COLOR_BGR2GRAY)
    haar_cascade_face = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    faces_rects = haar_cascade_face.detectMultiScale(test_image_gray, scaleFactor = 1.2, minNeighbors = 5)
    try:
        print(faces_rects[0])
    except:
        print('Ошибка при выводе массива координат лиц')
        return 'Ошибка. На изображении не найдено лиц.'
    for (x,y,w,h) in faces_rects:
        imageFilter.thumbnail((w*1.5,h*2), Image.ANTIALIAS)
        imageFilter.save('resizedFilter.png', quality = 100)
        resizedFilter = Image.open('resizedFilter.png')
        image.paste(imageFilter.convert('RGB'), (int(x-0.08*w), int(y-0.39*h)), imageFilter)
        print(x,y,w,h)

    image.save(changed_image_name)
    return str(changed_image_name)

def drawDogMask(img, chat_ID):
    changed_image_name = ('changed_' + str(chat_ID) + '.jpg')
    image = Image.open(img)
    imageFilter = Image.open('dogFilter.png')

    test_image = cv2.imread(img)
    image_copy = test_image.copy()
    test_image_gray = cv2.cvtColor(image_copy, cv2.COLOR_BGR2GRAY)
    haar_cascade_face = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    faces_rects = haar_cascade_face.detectMultiScale(test_image_gray, scaleFactor = 1.2, minNeighbors = 5)
    try:
        print(faces_rects[0])
    except:
        print('Ошибка при выводе массива координат лиц')
        return 'Ошибка. На изображении не найдено лиц.'
    for (x,y,w,h) in faces_rects:
        imageFilter.thumbnail((w*1.5,h*2), Image.ANTIALIAS)
        imageFilter.save('resizedFilter.png', quality = 100)
        resizedFilter = Image.open('resizedFilter.png')
        image.paste(imageFilter.convert('RGB'), (int(x-0.01*w), int(y-0.08*h)), imageFilter)
  
    image.save(changed_image_name)
    return str(changed_image_name)

def drawFoxMask(img, chat_ID):
    changed_image_name = ('changed_' + str(chat_ID) + '.jpg')
    image = Image.open(img)
    imageFilter = Image.open('foxFilter.png')

    test_image = cv2.imread(img)
    image_copy = test_image.copy()
    test_image_gray = cv2.cvtColor(image_copy, cv2.COLOR_BGR2GRAY)
    haar_cascade_face = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    faces_rects = haar_cascade_face.detectMultiScale(test_image_gray, scaleFactor = 1.2, minNeighbors = 5)
    try:
        print(faces_rects[0])
    except:
        print('Ошибка при выводе массива координат лиц')
        return 'Ошибка. На изображении не найдено лиц.'
    for (x,y,w,h) in faces_rects:
        imageFilter.thumbnail((w*2,h*2), Image.ANTIALIAS)
        imageFilter.save('resizedFilter.png', quality = 100)
        resizedFilter = Image.open('resizedFilter.png')
        image.paste(imageFilter.convert('RGB'), (int(x-0.08*w), int(y -0.08*h)), imageFilter)

    image.save(changed_image_name)
    return str(changed_image_name)