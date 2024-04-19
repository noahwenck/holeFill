import datetime
import sys
import timeit
sys.path.append('../')

logFile = open("../timeMeasurement/timeMeasurementLog.txt", "a")

numIterations = 200

setupStatement = """
import numpy as np
from PIL import Image
from scriptFunctions import (depthHoleFill, cameraMovementLeftRight, toleranceDepthFill)
pixels = np.array(Image.open("../images/largeDisocclusion/largeDisocclusion.png"))
depth = np.array(Image.open("../images/depth2c.png"))
"""

depthHoleFill = """
depthHoleFill(pixels, depth)
"""

cameraMovementLeftRight = """
cameraMovementLeftRight(pixels, depth)
"""

toleranceDepthFill = """
toleranceDepthFill(pixels, depth)
"""

holeFillWithDepthTimes = timeit.repeat(setup=setupStatement,
                                       stmt=depthHoleFill,
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

logFile.write("\n" + str(datetime.datetime.now()) + "\n" +
              str(numIterations) + " iterations\n")

logFile.write("\n--- Hole Fill with Depth --- \n")
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
