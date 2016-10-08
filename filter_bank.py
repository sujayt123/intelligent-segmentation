import numpy as np
import math

# Create 8 different filters to compute the appropriate intensity gradients perpendicular to each direction from a source pixel.
filter_bank = {}
filter_bank[(-1, -1)] = 1.0 / math.sqrt(2) * np.array([[0, 1, 0], [-1, 0, 0], [0, 0, 0]])
filter_bank[(-1, 0)] = 1.0 / 4 * np.array([[1, 0, -1], [1, 0, -1], [0, 0, 0]])
filter_bank[(-1, 1)] = 1.0 / math.sqrt(2) * np.array([[0, 1, 0], [0, 0, -1], [0, 0, 0]])
filter_bank[(0, -1)] = 1.0 / 4 * np.array([[1, 1, 0], [0, 0, 0], [-1, -1, 0]])
filter_bank[(0, 1)] = 1.0 / 4 * np.array([[0, 1, 1], [0, 0, 0], [0, -1, -1]])
filter_bank[(1, -1)] = 1.0 / math.sqrt(2) * np.array([[0, 0, 0], [1, 0, 0], [0, -1, 0]])
filter_bank[(1, 0)] = 1.0 / 4 * np.array([[0, 0, 0], [1, 0, -1], [1, 0, -1]])
filter_bank[(1, 1)] = 1.0 / math.sqrt(2) * np.array([[0, 0, 0], [0, 0, 1], [0, -1, 0]])