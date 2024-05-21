import sys


# This file is exclusively for Timeit purposes
# -- Excludes Image parsing and print statements --
# todo: if update any script, remember to add changes here too

def depthHoleFill(pixels, depth):
    height, width, channels = pixels.shape
    newImage = pixels.copy()

    for x in range(width):
        for y in range(height):
            # For now, 0 Alpha indicates hole pixel
            if pixels[y][x][3] == 0:
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
                        right = depth[y][sourceX][0]
                        rightPos = sourceX - x
                        break

                # Left
                for sourceX in range(x, 0, -1):
                    if pixels[y][sourceX][3] > 0:
                        left = depth[y][sourceX][0]
                        leftPos = x - sourceX
                        break

                # Top
                for sourceY in range(y, 0, -1):
                    if pixels[sourceY][x][3] > 0:
                        top = depth[sourceY][x][0]
                        topPos = y - sourceY
                        break

                # Bottom
                for sourceY in range(y, height):
                    if pixels[sourceY][x][3] > 0:
                        bottom = depth[sourceY][x][0]
                        bottomPos = sourceY - y
                        break

                # Diagonal Top-Right
                for sourceDiagR in range(x, width):
                    sourceDiagT = y - (sourceDiagR - x)
                    if pixels[sourceDiagT][sourceDiagR][3] > 0:
                        diagTR = depth[sourceDiagT][sourceDiagR][0]
                        diagTRPos = sourceDiagR - x
                        break

                # Diagonal Top-left
                for sourceDiagL in range(x, 0, -1):
                    sourceDiagT = y - (x - sourceDiagL)
                    if pixels[sourceDiagT][sourceDiagL][3] > 0:
                        diagTL = depth[sourceDiagT][sourceDiagL][0]
                        diagTLPos = x - sourceDiagL
                        break

                # Diagonal Bottom-Right
                for sourceDiagR in range(x, width):
                    sourceDiagB = y + (sourceDiagR - x)
                    if pixels[sourceDiagB][sourceDiagR][3] > 0:
                        diagBR = depth[sourceDiagB][sourceDiagR][0]
                        diagBRPos = sourceDiagR - x
                        break

                # Diagonal Bottom-Left
                for sourceDiagL in range(x, 0, -1):
                    sourceDiagB = y + (x - sourceDiagL)
                    if pixels[sourceDiagB][sourceDiagL][3] > 0:
                        diagBL = depth[sourceDiagB][sourceDiagL][0]
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


def noDepthHoleFill(pixels):
    height, width, channels = pixels.shape
    newImage = pixels.copy()

    for x in range(width):
        for y in range(height):
            # For now, 0 Alpha indicates hole pixel
            if pixels[y][x][3] == 0:
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


def cameraMovementLeftRight(pixels, depth):
    height, width, channels = pixels.shape
    newImage = pixels.copy()

    for x in range(width):
        for y in range(height):
            # For now, 0 Alpha indicates hole pixel
            if pixels[y][x][3] == 0:
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
                if top == minDepth:
                    newImage[y][x] = pixels[y - topPos][x]
                elif bottom == minDepth:
                    newImage[y][x] = pixels[y + bottomPos][x]


def toleranceDepthFill(pixels, depth):
    height, width, channels = pixels.shape
    newImage = pixels.copy()

    for x in range(width):
        for y in range(height):
            # For now, 0 Alpha indicates hole pixel
            if pixels[y][x][3] == 0:
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

                directionDepth = [right, left, top, bottom, diagTR, diagTL, diagBR, diagBL]
                directionDepth.sort()
                delta = 0.2  # Tolerance Delta
                frontDepth = directionDepth[7] + (directionDepth[7] * delta)
                midDepth = sys.maxsize

                # Find first direction that is past the depth tolerance
                for direction in directionDepth:
                    if direction > frontDepth:
                        midDepth = direction
                        break

                # If none are past the tolerance, use the farthest depth
                if midDepth == sys.maxsize:
                    midDepth = directionDepth[0]

                if right == midDepth:
                    newImage[y][x] = pixels[y][x + rightPos]
                elif left == midDepth:
                    newImage[y][x] = pixels[y][x - leftPos]
                elif top == midDepth:
                    newImage[y][x] = pixels[y - topPos][x]
                elif bottom == midDepth:
                    newImage[y][x] = pixels[y + bottomPos][x]
                elif diagTR == midDepth:
                    newImage[y][x] = pixels[y - diagTRPos][x + diagTRPos]
                elif diagTL == midDepth:
                    newImage[y][x] = pixels[y - diagTLPos][x - diagTLPos]
                elif diagBR == midDepth:
                    newImage[y][x] = pixels[y + diagBRPos][x + diagBRPos]
                elif diagBL == midDepth:
                    newImage[y][x] = pixels[y + diagBLPos][x - diagBLPos]


def toleranceAveragedDepthFill(pixels, depth):
    height, width, channels = pixels.shape
    newImage = pixels.copy()

    for x in range(width):
        for y in range(height):
            # For now, 0 Alpha indicates hole pixel
            if pixels[y][x][3] == 0:
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

                # Find the closest depth
                frontDepth = -1
                for direction in directionDepth.keys():
                    currentDepth = directionDepth.get(direction)
                    if currentDepth > frontDepth:
                        frontDepth = currentDepth

                # if frontDepth is still -1, cry

                frontDepth = frontDepth - (frontDepth * delta)

                # Find the nearest mid-ground depth
                # Prevents using a mid-depth that is extremely far away
                directionsToKeep = []
                for direction in directionDistance.keys():
                    if directionDepth.get(direction) >= frontDepth:
                        directionsToKeep.append(direction)

                shortestDirection = sys.maxsize
                shortestDirectionMapping = "t"
                for direction in directionDistance.keys():
                    if (direction not in directionsToKeep and
                            directionDistance.get(direction) <= shortestDirection):
                        directionsToKeep.append(direction)
                        shortestDirection = directionDistance.get(direction)
                        shortestDirectionMapping = direction

                midDepthLower = directionDepth.get(shortestDirectionMapping) - (
                        directionDepth.get(shortestDirectionMapping) * delta)
                for direction in directionDepth.keys():
                    if (direction not in directionsToKeep and
                            frontDepth > directionDepth.get(direction) >= midDepthLower):
                        directionsToKeep.append(direction)

                directionsToAverage = []
                for direction in directionsToKeep:
                    currentDepth = directionDepth.get(direction)
                    if midDepthLower <= currentDepth <= frontDepth:
                        directionsToAverage.append(direction)

                # # Find the closest depth that is beyond the tolerance
                # midDepthUpper = -1
                # for direction in directionDepth.keys():
                #     currentDepth = directionDepth.get(direction)
                #     if midDepthUpper < currentDepth < frontDepth:
                #         midDepthUpper = currentDepth
                #
                # # Gather a list of directions that are within the mid-ground tolerance,
                # # the values of these directions are what we will average
                # directionsToAverage = []
                # midDepthLower = midDepthUpper - (midDepthUpper * delta)
                # for direction in directionDepth.keys():
                #     currentDepth = directionDepth.get(direction)
                #     if midDepthLower <= currentDepth <= midDepthUpper:
                #         directionsToAverage.append(direction)

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
