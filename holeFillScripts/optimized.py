import sys
from PIL import Image
import numpy as np
from holeFillScripts.binaryPixelSearch import binaryPixelSearch
sys.path.append('../')

# IMAGE INPUT
pixels = np.array(Image.open("images/optimized/optimizedBase.png"))
height, width, channels = pixels.shape

newImage = pixels.copy()
rangeToBeChecked = 8  # Keep even

for x in range(width):
    for y in range(height):

        # Just doing right side no depth as an example.
        # Only right side to show the distance it can cover like this.
        # No depth since it doesn't matter with just one side, easy to implement depth.
        if pixels[y][x][3] == 0:
            for sourceX in range(x, width, rangeToBeChecked):
                # Found possible edge of hole
                if pixels[y][sourceX][3] > 0:
                    sourceX = binaryPixelSearch(pixels, y, sourceX - rangeToBeChecked, sourceX)
                    newImage[y][x] = pixels[y][sourceX]
                    print("Edge Pixel found at: (" + str(sourceX) + ", " + str(y) + ")")
                    break

# IMAGE OUTPUT
Image.fromarray(newImage, 'RGBA').save("images/optimized/optimizedResult.png", 'PNG')
