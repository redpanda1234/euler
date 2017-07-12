import math
import random

def TeX_gen(num_points, label = False):
    to_write = "\\documentclass[tikz, border=5pt]{standalone}\n"
    to_write += "\\usepackage{tikz}\n"
    to_write += "\\usepackage{tkz-euclide}\n"
    to_write += "\\begin{document}\n"
    to_write += "\\begin{tikzpicture}"
    max_val = int(math.floor(math.sqrt(num_points)))
    for i in range(num_points):
        x,y = [random.uniform(-max_val, max_val) for i in range(2)]
        x,y = round(x, 2), round(y,2)
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
        to_write += "at (" + str(x) +"," + str(y) + ") {};\n"
    max_str = str(max_val)
    to_write += "\\tkzInit[xmax="+max_str+",ymax="+max_str+",xmin=-"+max_str+",ymin=-"+max_str+"];\n"
    to_write += "\\tkzGrid;\n"
    to_write += "\\tkzAxeXY;\n"
    to_write += "\\end{tikzpicture}\n"
    to_write += "\\end{document}"
    file = open(str(num_points)+".tex", "w")
    file.write(to_write)
    file.close()
