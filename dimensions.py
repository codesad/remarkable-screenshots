import numpy as np

# reMarkable dimensions
RESOLUTION = (1650, 2260)
DIMENSIONS_CM = (15.8, 20.0)
DOTS_PER_CM = np.array(RESOLUTION) / np.array(DIMENSIONS_CM)
DOTS_PER_INCH = tuple(DOTS_PER_CM * 2.54)