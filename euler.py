import numpy as np
import math

import matplotlib.pyplot as plt

def derivative_x_squared(x):
    """
    """
    return 2*x


def euler(num_steps, step_size, initial_point = np.array([0.,0.]), derivative = derivative_x_squared):
    to_write = np.zeros((num_steps, 2))
    for n in range(num_steps):
        to_write[n] = initial_point
        initial_point += np.array([step_size, step_size*derivative(initial_point[0])])
    return to_write

plt.plot(euler(10,.5))
plt.show()
