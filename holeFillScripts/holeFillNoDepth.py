import sys
from PIL import Image
import numpy as np
sys.path.append('../')

# IMAGE INPUT
pixels = np.array(Image.open("images/hole.png"))
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
                if pixels[y][sourceX][3] > 0:
                    right = sourceX - x
                    break

            # Left
            for sourceX in range(x, 0, -1):
                if pixels[y][sourceX][3] > 0:
                    left = x - sourceX
                    break

            # Top
            for sourceY in range(y, 0, -1):
                if pixels[sourceY][x][3] > 0:
                    top = y - sourceY
                    break

            # Bottom
            for sourceY in range(y, height):
                if pixels[sourceY][x][3] > 0:
                    bottom = sourceY - y
                    break

            minDirection = min([right, left, top, bottom])
            if right == minDirection:
                newImage[y][x] = pixels[y][x + right]
            elif left == minDirection:
                newImage[y][x] = pixels[y][x - left]
            elif top == minDirection:
                newImage[y][x] = pixels[y - top][x]
            elif bottom == minDirection:
                newImage[y][x] = pixels[y + bottom][x]


# IMAGE OUTPUT
Image.fromarray(newImage, 'RGBA').save("images/resultNoDepth.png", 'PNG')
