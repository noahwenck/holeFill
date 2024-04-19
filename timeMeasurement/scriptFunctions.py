import sys

# This file is exclusively for Timeit purposes
# -- Excludes Image parsing and print statements --


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
