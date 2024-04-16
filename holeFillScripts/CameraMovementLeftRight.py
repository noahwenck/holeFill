import sys
from PIL import Image
import numpy as np
sys.path.append('../')

# IMAGE INPUT
pixels = np.array(Image.open("images/largeDisocclusion/disocclusionLarge.png"))
height, width, channels = pixels.shape

depth = np.array(Image.open("images/depth2.png"))

newImage = pixels.copy()


for x in range(width):
    for y in range(height):
        # For now, 0 Alpha indicates hole pixel
        if pixels[y][x][3] == 0:
            print("Filling pixel: (" + str(x) + ", " + str(y) + ")")
            top = sys.maxsize
            bottom = sys.maxsize

            # Top
            for sourceY in range(y, 0, -1):
                if pixels[sourceY][x][3] > 0:
                    top = depth[sourceY][x][1]
                    topPos = y - sourceY
                    break

            # Bottom
            for sourceY in range(y, height):
                if pixels[sourceY][x][3] > 0:
                    bottom = depth[sourceY][x][1]
                    bottomPos = sourceY - y
                    break

            minDepth = min(top, bottom)
            print("topDistance="+str(top)+", bottomDistance="+str(bottom))
            if top == minDepth:
                newImage[y][x] = pixels[y - topPos][x]
            elif bottom == minDepth:
                newImage[y][x] = pixels[y + bottomPos][x]


# IMAGE OUTPUT
Image.fromarray(newImage, 'RGBA').save("images/largeDisocclusion/CameraMovementLeftRightResult.png", 'PNG')