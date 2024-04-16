import sys
from PIL import Image
import numpy as np
sys.path.append('../')

# IMAGE INPUT
pixels = np.array(Image.open("images/largeDisocclusion/disocclusionLarge.png"))
height, width, channels = pixels.shape

depth = np.array(Image.open("images/depth.png"))

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
                    right = depth[y][sourceX]
                    rightPos = sourceX - x
                    break

            # Left
            for sourceX in range(x, 0, -1):
                if pixels[y][sourceX][3] > 0:
                    left = depth[y][sourceX]
                    leftPos = x - sourceX
                    break

            # Top
            for sourceY in range(y, 0, -1):
                if pixels[sourceY][x][3] > 0:
                    top = depth[sourceY][x]
                    topPos = y - sourceY
                    break

            # Bottom
            for sourceY in range(y, height):
                if pixels[sourceY][x][3] > 0:
                    bottom = depth[sourceY][x]
                    bottomPos = sourceY - y
                    break

            # Diagonal Top-Right
            for sourceDiagR in range(x, width):
                sourceDiagT = y - (sourceDiagR - x)
                if pixels[sourceDiagT][sourceDiagR][3] > 0:
                    diagTR = depth[sourceDiagT][sourceDiagR]
                    diagTRPos = sourceDiagR - x
                    break

            # Diagonal Top-left
            for sourceDiagL in range(x, 0, -1):
                sourceDiagT = y - (x - sourceDiagL)
                if pixels[sourceDiagT][sourceDiagL][3] > 0:
                    diagTL = depth[sourceDiagT][sourceDiagL]
                    diagTLPos = x - sourceDiagL
                    break

            # Diagonal Bottom-Right
            for sourceDiagR in range(x, width):
                sourceDiagB = y + (sourceDiagR - x)
                if pixels[sourceDiagB][sourceDiagR][3] > 0:
                    diagBR = depth[sourceDiagB][sourceDiagR]
                    diagBRPos = sourceDiagR - x
                    break

            # Diagonal Bottom-Left
            for sourceDiagL in range(x, 0, -1):
                sourceDiagB = y + (x - sourceDiagL)
                if pixels[sourceDiagB][sourceDiagL][3] > 0:
                    diagBL = depth[sourceDiagB][sourceDiagL]
                    diagBLPos = x - sourceDiagL
                    break

            minDepth = min(right, left, top, bottom, diagTR, diagTL, diagBR, diagBL)
            if right == minDepth:
                newImage[y][x] = pixels[y][x + rightPos]
            elif left == minDepth:
                newImage[y][x] = pixels[y][x - leftPos]
            elif top == minDepth:
                newImage[y][x] = pixels[y - topPos][x]
            elif bottom == minDepth:
                newImage[y][x] = pixels[y + bottomPos][x]
            elif diagTR == minDepth:
                newImage[y][x] = pixels[y - diagTRPos][x + diagTRPos]
            elif diagTL == minDepth:
                newImage[y][x] = pixels[y - diagTLPos][x - diagTLPos]
            elif diagBR == minDepth:
                newImage[y][x] = pixels[y + diagBRPos][x + diagBRPos]
            elif diagBL == minDepth:
                newImage[y][x] = pixels[y + diagBLPos][x - diagBLPos]


# IMAGE OUTPUT
Image.fromarray(newImage, 'RGBA').save("images/largeDisocclusion/baseDepthResult.png", 'PNG')
