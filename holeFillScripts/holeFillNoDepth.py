import sys
from PIL import Image
import numpy as np
sys.path.append('../')

# IMAGE INPUT
pixels = np.array(Image.open("INSERT_SOURCE_FILENAME"))
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

            # Diagonal Top-Right
            for sourceDiagR in range(x, width):
                sourceDiagT = y - (sourceDiagR - x)
                if pixels[sourceDiagT][sourceDiagR][3] > 0:
                    diagTR = sourceDiagR - x
                    break

            # Diagonal Top-left
            for sourceDiagL in range(x, 0, -1):
                sourceDiagT = y - (x - sourceDiagL)
                if pixels[sourceDiagT][sourceDiagL][3] > 0:
                    diagTL = x - sourceDiagL
                    break

            # Diagonal Bottom-Right
            for sourceDiagR in range(x, width):
                sourceDiagB = y + (sourceDiagR - x)
                if pixels[sourceDiagB][sourceDiagR][3] > 0:
                    diagBR = sourceDiagR - x
                    break

            # Diagonal Bottom-Left
            for sourceDiagL in range(x, 0, -1):
                sourceDiagB = y + (x - sourceDiagL)
                if pixels[sourceDiagB][sourceDiagL][3] > 0:
                    diagBL = x - sourceDiagL
                    break

            minDirection = min([right, left, top, bottom, diagBL, diagTL, diagBL, diagTR])
            if right == minDirection:
                newImage[y][x] = pixels[y][x + right]
            elif left == minDirection:
                newImage[y][x] = pixels[y][x - left]
            elif top == minDirection:
                newImage[y][x] = pixels[y - top][x]
            elif bottom == minDirection:
                newImage[y][x] = pixels[y + bottom][x]
            elif diagTR == minDirection:
                newImage[y][x] = pixels[y - diagTR][x + diagTR]
            elif diagTL == minDirection:
                newImage[y][x] = pixels[y - diagTL][x - diagTL]
            elif diagBR == minDirection:
                newImage[y][x] = pixels[y + diagBR][x + diagBR]
            elif diagBL == minDirection:
                newImage[y][x] = pixels[y + diagBL][x - diagBL]


# IMAGE OUTPUT
Image.fromarray(newImage, 'RGBA').save("INSERT_RESULT_FILENAME", 'PNG')
