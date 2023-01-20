from PIL import Image
import math
import os
from pathlib import Path

def comimg(image):
    img = Image.open(image)
    x, y = img.size
    img = img.resize((math.floor(x),math.floor(y)),Image.ANTIALIAS)
    img.save(image, quality=50)

jpgImages = Path("./").glob("*.jpg")
pngImages = Path("./").glob("*.png")
images = [str(p) for p in jpgImages] + [str(p) for p in pngImages]

for i in range(len(images)):
    comimg(images[i])
    os.system("cls")
    print(f"{i+1}/{len(images)}")

print("DONE!!!")