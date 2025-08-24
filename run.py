from PIL import Image
import math
import os
from pathlib import Path


def png2jpg(image):
    img = Image.open(image)
    img = img.convert('RGB')
    img.save(f'{image[:-4]}.jpg')
    os.remove(image)


def comimg(image):
    img = Image.open(image)
    x, y = img.size
    img = img.resize((math.floor(x),math.floor(y)),Image.ANTIALIAS)
    img.save(image, quality=25)


pngImages = Path("./").glob("*.png")
pngImages = [str(p) for p in pngImages]
for i in range(len(pngImages)):
    png2jpg(pngImages[i])

jpgImages = Path("./").glob("*.jpg")
images = [str(p) for p in jpgImages]
# images = [str(p) for p in jpgImages] + [str(p) for p in pngImages]

for i in range(len(images)):
    comimg(images[i])
    os.system("cls")
    print(f"{i+1}/{len(images)}")

print("DONE!!!")