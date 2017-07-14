import math
import random
import numpy as np

def gen_tex(num_points, centroid_lines = True, label = False):
    to_write = "\\documentclass[tikz, border=5pt]{standalone}\n"
    to_write += "\\usepackage{tikz}\n"
    to_write += "\\usepackage{tkz-euclide}\n"
    to_write += "\\begin{document}\n"
    to_write += "\\begin{tikzpicture}\n"
    max_val = int(math.floor(math.sqrt(num_points)))
    centroid = np.array([0.,0.])
    node_list = []
    for i in range(num_points):
        x,y = [random.uniform(-max_val, max_val) for i in range(2)]
        x,y = round(x, 2), round(y,2)
        centroid += np.array([x,y])
        if label:
            if x>=0 and y>=0:
                label = "label=above right:"
            elif x<0 and y>=0:
                label = "label=above left:"
            elif x<0 and y<0:
                label = "label=below left:"
            else:
                label = "label=below right:"
            label += "{$(" + str(x) +","+ str(y)+")$}"
        else:
            label = ""
        to_write += "\\node[draw,circle,fill,inner sep = 1pt," + label +"]"
        to_write += "(" + str(i) + ") at (" + str(x) +"," + str(y) + ") {};\n"
        node_list += [i]
    centroid /= num_points
    to_write += "\\node[draw, circle, fill, inner sep = 1pt, color=blue] (centroid) at (" + str(centroid[0]) + "," + str(centroid[1]) + ") {};\n"
    if centroid_lines:
        for i in node_list:
            to_write += "\\draw[dotted] (" + str(i) + ") -- (centroid);\n"
    max_str = str(max_val)
    to_write += "\\tkzInit[xmax="+max_str+",ymax="+max_str+",xmin=-"+max_str+",ymin=-"+max_str+"];\n"
    to_write += "\\tkzGrid;\n"
    to_write += "\\tkzAxeXY;\n"
    to_write += "\\end{tikzpicture}\n"
    to_write += "\\end{document}"
    file = open(str(num_points)+".tex", "w")
    file.write(to_write)
    file.close()

def derivative_x_squared(x):
    """Returns the derivative of x^2 (2*x) at the input."""
    return 2*x

def euler(
    num_steps, step_size,
    initial_point=np.array([0.,0.]),
    derivative_function=derivative_x_squared
    ):
    """
    Implements euler’s method for the input function.

    Performs numerical integration over a finite amount of
    steps, by approximating the function with the tangent
    line. Parameters below described in the format
    <datatype, description>

    Parameters
    ----------
    num_steps : int, describes the number of steps to take.
                for a fixed step size, higher num_steps will
                increase the amount of the function our
                approximation covers.

    step_size : float, describes the size of each step.
                Higher step size will increase the amount of
                the function that the approximation covers
                (for fixed num_steps), but at the cost of
                accuracy.

    initial_point : numpy array, describes the initial
                    condition.  Order is (x,y).  Defaults
                    to np.array([0.,0.]).  Datatype stored
                    in the array should be float.

    derivative_function : function, calculates the derivative
                          of the mathematical function we’re
                          integrating.  Should take inputs
                          either of type int or type float.
                          defaults to derivative_x_squared,
                          which returns 2*x.

    Returns
    -------
    out_array : numpy array, entries are other objects of type
                numpy array.

    """
    #<some code here>
    return #some array
