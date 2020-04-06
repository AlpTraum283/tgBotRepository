from PIL import Image

btnList = {
    'Повернуть на 90° влево': 'imageRotateLeft'
}

def imageRotateLeft(fileName):
    image = Image.open(fileName)
    rotated_image = image.rotate(90, expand = True)
    rotated_image.save('rotated_image.jpg', quality = 100)
    return 'rotated_image.jpg'