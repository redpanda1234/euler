import numpy as np
from scipy import integrate

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import cnames
from matplotlib import animation

import time



def animate(i):
    # we'll step two time-steps per frame.  This leads to nice results.
    steps = 4
    i = (steps * i) % x_t.shape[1]
    for line, pt, xi in zip(lines, pts, x_t):
        x, y, z = xi[:i].T
        line.set_data(x, y)
        line.set_3d_properties(z)

        pt.set_data(x[-1:], y[-1:])
        pt.set_3d_properties(z[-1:])
    ax.view_init(30, 0.3 * i)
    fig.canvas.draw()
    return lines + pts

start_time = time.time()
# instantiate the animator.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=6000, interval=30, blit=True)
mywriter = animation.FFMpegWriter()
anim.save('chaotic_initialcondition.mp4', writer='ffmpeg', fps=60, extra_args=['-vcodec', 'libx264'], bitrate=8000)
print("saved the file!")
plt.show()

print("runtime is", time.time()-start_time)
