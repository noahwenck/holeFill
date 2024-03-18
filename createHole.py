from PIL import Image
import numpy as np

# IMAGE INPUT
# open image (where `img_filename` is a string – e.g. "my_image.png")
img = Image.open("images/anAutumnAfternoon.png")
# get pixels as a numpy array
pixels = np.array(img)
# get resolution of image
height, width, channels = pixels.shape


for x in range(125, 145):
    for y in range(320, 350):
        pixels[y][x] = [0, 0, 0, 0]


# IMAGE OUTPUT
# create new image from numpy array
img_out = Image.fromarray(pixels, 'RGBA')
# save image (where `output_filename` is a string – e.g. "out_image.png")
img_out.save("images/hole.png", 'PNG')