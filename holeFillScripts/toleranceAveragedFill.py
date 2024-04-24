import sys
from PIL import Image
import numpy as np
sys.path.append('../')

# IMAGE INPUT
pixels = np.array(Image.open("../images/anAutumnAfternoon/largeDisocclusion.png"))
height, width, channels = pixels.shape

depth = np.array(Image.open("../images/anAutumnAfternoon/depth/depth2c.png"))

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
                    right = depth[y][sourceX][1]
                    rightPos = sourceX - x
                    break

            # Left
            for sourceX in range(x, 0, -1):
                if pixels[y][sourceX][3] > 0:
                    left = depth[y][sourceX][1]
                    leftPos = x - sourceX
                    break

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

            # Diagonal Top-Right
            for sourceDiagR in range(x, width):
                sourceDiagT = y - (sourceDiagR - x)
                if pixels[sourceDiagT][sourceDiagR][3] > 0:
                    diagTR = depth[sourceDiagT][sourceDiagR][1]
                    diagTRPos = sourceDiagR - x
                    break

            # Diagonal Top-left
            for sourceDiagL in range(x, 0, -1):
                sourceDiagT = y - (x - sourceDiagL)
                if pixels[sourceDiagT][sourceDiagL][3] > 0:
                    diagTL = depth[sourceDiagT][sourceDiagL][1]
                    diagTLPos = x - sourceDiagL
                    break

            # Diagonal Bottom-Right
            for sourceDiagR in range(x, width):
                sourceDiagB = y + (sourceDiagR - x)
                if pixels[sourceDiagB][sourceDiagR][3] > 0:
                    diagBR = depth[sourceDiagB][sourceDiagR][1]
                    diagBRPos = sourceDiagR - x
                    break

            # Diagonal Bottom-Left
            for sourceDiagL in range(x, 0, -1):
                sourceDiagB = y + (x - sourceDiagL)
                if pixels[sourceDiagB][sourceDiagL][3] > 0:
                    diagBL = depth[sourceDiagB][sourceDiagL][1]
                    diagBLPos = x - sourceDiagL
                    break

            delta = 0.3  # Tolerance Delta
            # todo: make into one map?
            directionDepth = {
                "r": right,
                "br": diagBR,
                "b": bottom,
                "bl": diagBL,
                "l": left,
                "tl": diagTL,
                "t": top,
                "tr": diagTR
            }
            directionColor = {
                "r": pixels[y][x + rightPos],
                "br": pixels[y + diagBRPos][x + diagBRPos],
                "b": pixels[y + bottomPos][x],
                "bl": pixels[y + diagBLPos][x - diagBLPos],
                "l": pixels[y][x - leftPos],
                "tl": pixels[y - diagTLPos][x - diagTLPos],
                "t": pixels[y - topPos][x],
                "tr": pixels[y - diagTRPos][x + diagTRPos]
            }

            # Find the closest depth
            frontDepth = -1
            for direction in directionDepth.keys():
                currentDepth = directionDepth.get(direction)
                if currentDepth > frontDepth:
                    frontDepth = currentDepth

            # if frontDepth is still -1, cry

            frontDepth = frontDepth - (frontDepth * delta)

            # Find the closest depth that is beyond the tolerance
            midDepthUpper = -1
            for direction in directionDepth.keys():
                currentDepth = directionDepth.get(direction)
                if midDepthUpper < currentDepth < frontDepth:
                    midDepthUpper = currentDepth

            # Gather a list of directions that are within the mid-ground tolerance,
            # the values of these directions are what we will average
            directionsToAverage = []
            midDepthLower = midDepthUpper - (midDepthUpper * delta)
            for direction in directionDepth.keys():
                currentDepth = directionDepth.get(direction)
                if midDepthLower <= currentDepth <= midDepthUpper:
                    directionsToAverage.append(direction)

            # this is fine
            averageColor = [0, 0, 0, 0]
            for direction in directionsToAverage:
                currentColor = directionColor.get(direction)
                averageColor[0] += currentColor[0]
                averageColor[1] += currentColor[1]
                averageColor[2] += currentColor[2]

            if averageColor != [0, 0, 0, 0]:
                averageColor = [averageColor[0] / len(directionsToAverage),
                                averageColor[1] / len(directionsToAverage),
                                averageColor[2] / len(directionsToAverage),
                                255]
                newImage[y][x] = averageColor
            else:
                # Make red to indicate something went wrong
                # This may also show that there is no direction that fits within the mid-ground tol
                newImage[y][x] = [255, 0, 0, 255]

Image.fromarray(newImage, 'RGBA').save("../images/anAutumnAfternoon/results/toleranceAveragedResult.png", 'PNG')
