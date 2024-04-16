import datetime
import sys
import timeit
sys.path.append('../')

logFile = open("timeMeasurement/timeMeasurementLog.txt", "a")

numIterations = 100

holeFillWithDepthTimes = timeit.repeat(stmt=open("holeFillScripts/holeFillWithDepth.py").read(), repeat=numIterations, number=1)
cameraMovementLRTimes = timeit.repeat(stmt=open("holeFillScripts/CameraMovementLeftRight.py").read(), repeat=numIterations, number=1)
toleranceDepthFillTimes = timeit.repeat(stmt=open("holeFillScripts/toleranceDepthFill.py").read(), repeat=numIterations, number=1)

logFile.write("\n" + str(datetime.datetime.now()) + " run\n" +
              str(numIterations) + " iterations (w/o print statements)\n")

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
