from PIL import Image
import numpy as np
from binaryPixelSearch import binaryPixelSearch

# IMAGE INPUT
pixels = np.array(Image.open("images/optimizedBase.png"))
height, width, channels = pixels.shape

# Hard-coded for optimizedBase.png example
x = 136
y = 325
rangeToBeChecked = 8 # Keep even

for sourceX in range(x, width, rangeToBeChecked):
    # Found possible edge of hole
    if pixels[y][sourceX][3] > 0:
        sourceX = binaryPixelSearch(pixels, y, sourceX-rangeToBeChecked, sourceX)
        break

print("Edge Pixel found at: (" + str(sourceX) + ", " + str(y) + ")")
pixels[y][x] = pixels[y][sourceX]

# IMAGE OUTPUT
Image.fromarray(pixels, 'RGBA').save("images/optimizedResult.png", 'PNG')
