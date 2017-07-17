import numpy as np
import math
import matplotlib.cm as cm
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

def derivative_x_squared(x):
    """Returns the derivative of x^2 (2*x) at the input."""
    return 2*x

def get_com(point_array):
    total = np.array([0.,0.])
    for point in point_array:
        total += point
    return total/len(point_array)

def lorentz_deriv(coord, sigma=10., beta=8./3, rho=28.0):
    """Compute the time-derivative of a Lorentz system."""
    coord = [1,2,3]
    x, y, z = coord # unpack coordinates
    return np.array([sigma * (y - x), x * (rho - z) - y, x * y - beta * z])

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

#vals = euler(20,.25, initial_point=np.array([0.,0.]))
#print(vals)
#x,y = [val[0] for val in vals], [val[1] for val in vals]
#print(x,y)
#val2 = np.array([np.array([x, np.sin(x)]) for x in np.linspace(0,np.pi,10000)])
#print("com of sin is", get_com(val2))
#plt.plot(x,y, "o")
#plt.show()

x = np.linspace(0,2*np.pi, 50) # this is similar to range()
y = np.cos(x)
y2 = y**2
plt.plot(x,y,"bo") # creates the plot with blue circle markers
plt.plot(x,y2,"g^") # same but green triangles pointing upward
plt.show()
