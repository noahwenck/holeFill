import datetime
import sys
import timeit
sys.path.append('../')
sys.dont_write_bytecode = True

logFile = open("../timeMeasurement/timeMeasurementLog.txt", "a")

numIterations = 50

# reminder to self to add import new functions in this block
setupStatement = """
import numpy as np
from PIL import Image
from scriptFunctions import (depthHoleFill, noDepthHoleFill, cameraMovementLeftRight, toleranceDepthFill, middleGroundAverage)
pixels = np.array(Image.open("IMAGEPATH"))
#depth = np.array(Image.open("IMAGEPATH"))
"""

depthHoleFill = """
depthHoleFill(pixels, depth)
"""

noDepthHoleFill = """
noDepthHoleFill(pixels)
"""

cameraMovementLeftRight = """
cameraMovementLeftRight(pixels, depth)
"""

toleranceDepthFill = """
toleranceDepthFill(pixels, depth)
"""

MiddleGroundAverageFill = """
middleGroundAverage(pixels, depth)
"""

holeFillWithDepthTimes = timeit.repeat(setup=setupStatement,
                                       stmt=depthHoleFill,
                                       repeat=numIterations,
                                       number=1)
holeFillNoDepthTimes = timeit.repeat(setup=setupStatement,
                                     stmt=noDepthHoleFill,
                                     repeat=numIterations,
                                     number=1)
cameraMovementLRTimes = timeit.repeat(setup=setupStatement,
                                      stmt=cameraMovementLeftRight,
                                      repeat=numIterations,
                                      number=1)
toleranceDepthFillTimes = timeit.repeat(setup=setupStatement,
                                        stmt=toleranceDepthFill,
                                        repeat=numIterations,
                                        number=1)
middleGroundAverageFillTimes = timeit.repeat(setup=setupStatement,
                                             stmt=MiddleGroundAverageFill,
                                             repeat=numIterations,
                                             number=1)

logFile.write("\n=========================\n" +
              str(datetime.datetime.now()) + "\n" +
              str(numIterations) + " iterations\n")

logFile.write("\n--- 8-Directional without Depth --- \n")
logFile.write("Min: " + str(min(holeFillNoDepthTimes)) + "\n")
logFile.write("Avg: " + str(sum(holeFillNoDepthTimes)/len(holeFillNoDepthTimes)) + "\n")
logFile.write("Max: " + str(max(holeFillNoDepthTimes)) + "\n")

logFile.write("\n--- 8-Directional with Depth --- \n")
logFile.write("Min: " + str(min(holeFillWithDepthTimes)) + "\n")
logFile.write("Avg: " + str(sum(holeFillWithDepthTimes)/len(holeFillWithDepthTimes)) + "\n")
logFile.write("Max: " + str(max(holeFillWithDepthTimes)) + "\n")

logFile.write("\n--- Camera Movement L / R --- \n")
logFile.write("Min: " + str(min(cameraMovementLRTimes)) + "\n")
logFile.write("Avg: " + str(sum(cameraMovementLRTimes)/len(cameraMovementLRTimes)) + "\n")
logFile.write("Max: " + str(max(cameraMovementLRTimes)) + "\n")

logFile.write("\n--- Tolerance Depth --- \n")
logFile.write("Min: " + str(min(toleranceDepthFillTimes)) + "\n")
logFile.write("Avg: " + str(sum(toleranceDepthFillTimes)/len(toleranceDepthFillTimes)) + "\n")
logFile.write("Max: " + str(max(toleranceDepthFillTimes)) + "\n")

logFile.write("\n--- Tolerance Averaged Depth --- \n")
logFile.write("Min: " + str(min(middleGroundAverageFillTimes)) + "\n")
logFile.write("Avg: " + str(sum(middleGroundAverageFillTimes)/len(middleGroundAverageFillTimes)) + "\n")
logFile.write("Max: " + str(max(middleGroundAverageFillTimes)) + "\n")
