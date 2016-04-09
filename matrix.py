import json
import numpy
from basics import combat

num_creatures = len(creature_list)

# matrix[attack][block]
matrix = numpy.zeros((num_creatures, num_creatures), dtype=int)

for x in range(num_creatures):
    for y in range(num_creatures):
        matrix[x][y] = combat(x, y).value

"""
from matplotlib import pyplot as plt
heatmap = plt.pcolor(matrix)
plt.show()
"""
