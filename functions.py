from PIL import Image

btnList = {
    'Повернуть на 90° влево': 'imageRotateLeft'
}

def imageRotateLeft(fileName,chat_ID):
    rotated_image_name = ('rotated_' + str(chat_ID) + '.jpg')
    image = Image.open(fileName)
    rotated_image = image.rotate(90, expand = True)
    rotated_image.save(rotated_image_name, quality = 100)
    return str(rotated_image_name)