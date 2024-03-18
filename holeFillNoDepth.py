import sys
from PIL import Image
import numpy as np

# IMAGE INPUT
# open image (where `img_filename` is a string – e.g. "my_image.png")
img = Image.open("images/hole.png")
# get pixels as a numpy array
pixels = np.array(img)
# get resolution of image
height, width, channels = pixels.shape

newImage = pixels.copy()


for x in range(width):
    for y in range(height):
        # For now, 0 Alpha indicates hole pixel
        if pixels[y][x][3] == 0:
            print("Filling pixel: (" + str(x) + ", " + str(y) + ")")
            right = sys.maxsize
            left = sys.maxsize
            top = sys.maxsize
            bottom = sys.maxsize

            # Right
            for sourceX in range(x, width):
                if pixels[y][sourceX][0] > 0:
                    right = sourceX - x
                    break

            # Left
            for sourceX in range(x, 0, -1):
                if pixels[y][sourceX][0] > 0:
                    left = x - sourceX
                    break

            # Top
            for sourceY in range(y, 0, -1):
                if pixels[sourceY][x][0] > 0:
                    top = y - sourceY
                    break

            # Bottom
            for sourceY in range(y, height):
                if pixels[sourceY][x][0] > 0:
                    bottom = sourceY - y
                    break

            potentialX = min(left, right)
            potentialY = min(top, bottom)
            if potentialX <= potentialY:
                if right <= left:
                    newImage[y][x] = pixels[y][x + potentialX]
                else:
                    newImage[y][x] = pixels[y][x - potentialX]
            else:
                if top <= bottom:
                    newImage[y][x] = pixels[y - potentialY][x]
                else:
                    newImage[y][x] = pixels[y + potentialY][x]


# IMAGE OUTPUT
# create new image from numpy array
img_out = Image.fromarray(newImage, 'RGBA')
# save image (where `output_filename` is a string – e.g. "out_image.png")
img_out.save("images/result.png", 'PNG')
