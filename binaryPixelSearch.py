def binaryPixelSearch(pixels, y, low, high):
    if low == high:
        return low

    mid = int((high + low) / 2)
    if pixels[y][mid][3] > 0:
        return binaryPixelSearch(pixels, y, low, mid)
    else:
        return binaryPixelSearch(pixels, y, mid+1, high)
