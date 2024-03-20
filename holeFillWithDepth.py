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
            diagTL = sys.maxsize
            diagTR = sys.maxsize
            diagBR = sys.maxsize
            diagBL = sys.maxsize

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

            # # Diagonal Top-Right
            # for sourceDiagR in range(x, width):
            #     sourceDiagT = y - 1
            #     if pixels[sourceDiagT][sourceDiagR][3] > 0:
            #         diagTR = sourceDiagR - x
            #         break
            #
            # # Diagonal Top-left
            # for sourceDiagL in range(x, 0, -1):
            #     sourceDiagT = y - 1
            #     if pixels[sourceDiagT][sourceDiagL][3] > 0:
            #         diagTL = x - sourceDiagL
            #         break
            #
            # # Diagonal Bottom-Right
            # for sourceDiagR in range(x, width):
            #     sourceDiagB = y + 1
            #     if pixels[sourceDiagB][sourceDiagR][3] > 0:
            #         diagBR = sourceDiagR - x
            #         break
            #
            # # Diagonal Bottom-Left
            # for sourceDiagL in range(x, 0, -1):
            #     sourceDiagB = y + 1
            #     if pixels[sourceDiagB][sourceDiagL][3] > 0:
            #         diagBL = x - sourceDiagL
            #         break

            potentialX = min(left, right)
            potentialY = min(top, bottom)
            minDirection = min([right, left, top, bottom, diagTR, diagTL, diagBR, diagBL])
            if right == minDirection:
                newImage[y][x] = pixels[y][x + right]
            elif left == minDirection:
                newImage[y][x] = pixels[y][x - left]
            elif top == minDirection:
                newImage[y][x] = pixels[y - top][x]
            elif bottom == minDirection:
                newImage[y][x] = pixels[y + bottom][x]
            # elif diagTR == minDirection:
            #     newImage[y][x] = pixels[y - diagTL][x + diagTL]
            # elif diagTL == minDirection:
            #     newImage[y][x] = pixels[y - diagTL][x - diagTL]
            # elif diagBR == minDirection:
            #     newImage[y][x] = pixels[y + diagTL][x + diagTL]
            # elif diagBL == minDirection:
            #     newImage[y][x] = pixels[y + diagTL][x - diagTL]


# IMAGE OUTPUT
# create new image from numpy array
img_out = Image.fromarray(newImage, 'RGBA')
# save image (where `output_filename` is a string – e.g. "out_image.png")
img_out.save("images/result.png", 'PNG')
