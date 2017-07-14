import numpy as np
import math
import matplotlib.pyplot as plt

def derivative_x_squared(x):
    """Returns the derivative of x^2 (2*x) at the input."""
    return 2*x

def euler(
        num_steps,
        step_size,
        initial_point=np.array([0.,0.]),
        derivative_function=derivative_x_squared
    ):
    """
    Implements euler’s method for the input function.

    Performs numerical integration over a finite amount of steps, by
    approximating the function with the tangent line. Parameters below
    described in the format <datatype, description>

    ----------
    Parameters
    ----------
    num_steps : int, describes the number of steps to take. For a
                fixed step size, higher num_steps will increase the
                amount of the function our approximation covers.

    step_size : float, describes the size of each step.  Higher step
                size will increase the amount of the function that the
                approximation covers (for fixed num_steps), but at the
                cost of accuracy.

    initial_point : numpy array, describes the initial condition.
                    Order is (x,y).  Defaults to np.array([0.,0.]).
                    Datatype stored in the array should be float.

    derivative_function : function, calculates the derivative of the
                          mathematical function we're integrating.
                          Should take inputs either of type int or type
                          float. Defaults to derivative_x_squared,
                          which returns 2*x.

    -------
    Returns
    -------
    out_array : numpy array, entries are other objects of type numpy
                array.  Each entry should describe some point (x,y)
                lying on our curve approximation.

    ------------
    Example call
    ------------
    point_array = euler(50, .25, initial_point=np.array([1.0,0.24]),
                        derivative_function = math.cos)
    """
    to_write = np.zeros((num_steps, 2))
    for n in range(num_steps):
        to_write[n] = initial_point
        initial_point += np.array([step_size, step_size*derivative_function(initial_point[0])])
    return to_write

print(euler(30, .5, initial_point = np.array([1.5,2.0]), derivative_function = lambda x : x**(3/2)))
print(euler(10, .25, initial_point = np.array([0.,0.]), derivative_function = lambda x : 2*x))

#plt.plot(euler(2,.5, initial_point=np.array([0.,0.])))

#plt.show()
