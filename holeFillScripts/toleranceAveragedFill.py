import sys
from PIL import Image
import numpy as np

sys.path.append('../')

# IMAGE INPUT
pixels = np.array(Image.open("../images/smokeStacksDisocclusion.png"))
height, width, channels = pixels.shape

depth = np.array(Image.open("../images/smokeStacksDepth.png"))

newImage = pixels.copy()

for x in range(width):
    for y in range(height):
        # For now, 0 Alpha indicates hole pixel
        if pixels[y][x][3] == 0:
            # print("Filling pixel: (" + str(x) + ", " + str(y) + ")")
            right = sys.maxsize
            left = sys.maxsize
            top = sys.maxsize
            bottom = sys.maxsize
            diagTL = sys.maxsize
            diagTR = sys.maxsize
            diagBR = sys.maxsize
            diagBL = sys.maxsize

            diagBLPos = -1
            leftPos = -1
            diagTLPos = -1

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

            delta = 0.1  # Tolerance Delta
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
            directionDistance = {
                "r": rightPos,
                "br": diagBRPos,
                "b": bottomPos,
                "bl": diagBLPos,
                "l": leftPos,
                "tl": diagTLPos,
                "t": topPos,
                "tr": diagTRPos
            }

            # Find first closet pixel
            shortestDirection = sys.maxsize
            shortestDirectionMapping = "t"
            for direction in directionDistance.keys():
                if directionDistance.get(direction) < shortestDirection:
                    shortestDirection = directionDistance.get(direction)
                    shortestDirectionMapping = direction

            # Find all pixels that are within our delta of this first pixel
            firstDepthUpper = directionDepth.get(shortestDirectionMapping) + (
                    directionDepth.get(shortestDirectionMapping) * delta)
            firstDepthLower = directionDepth.get(shortestDirectionMapping) - (
                    directionDepth.get(shortestDirectionMapping) * delta)
            firstDepthDirections = []
            for direction in directionDepth.keys():
                if firstDepthLower <= directionDepth.get(direction) < firstDepthUpper:
                    firstDepthDirections.append(direction)

            # Find the next closest pixel, not considering any that are in our first depth range
            nextShortestDirection = sys.maxsize
            nextShortestDirectionMapping = "t"
            for direction in directionDistance.keys():
                if (direction not in firstDepthDirections and
                        directionDistance.get(direction) < nextShortestDirection):
                    nextShortestDirection = directionDistance.get(direction)
                    nextShortestDirectionMapping = direction

            # In case all directions are already in firstDepthDirections
            if nextShortestDirection != sys.maxsize:

                # Find all pixels that are within our delta of this next pixel
                secondDepthUpper = directionDepth.get(nextShortestDirectionMapping) + (
                        directionDepth.get(nextShortestDirectionMapping) * delta)
                secondDepthLower = directionDepth.get(nextShortestDirectionMapping) - (
                        directionDepth.get(nextShortestDirectionMapping) * delta)
                secondDepthDirections = []
                for direction in directionDepth.keys():
                    if (direction not in firstDepthDirections and
                            secondDepthLower <= directionDepth.get(direction) <= secondDepthUpper):
                        secondDepthDirections.append(direction)

                # Whichever upper limit is highest, use those values for the average
                if firstDepthUpper < secondDepthUpper:
                    directionsToAverage = firstDepthDirections
                else:
                    directionsToAverage = secondDepthDirections
            else:
                directionsToAverage = firstDepthDirections

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
                newImage[y][x] = [0, 0, 0, 0]

Image.fromarray(newImage, 'RGBA').save("../images/smokeStacksResultToleranceAveraged.png", "PNG")
