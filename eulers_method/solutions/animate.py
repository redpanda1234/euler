# Almost all of this was written by Jake Vanderplas, here: https://jakevdp.github.io/blog/2013/02/16/animating-the-lorentz-system-in-3d/


import numpy as np

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import cnames
from matplotlib import animation

import euler

N_trajectories = 20

# Choose random starting points, uniformly distributed from -15 to 15
np.random.seed(1)
x0 = -15 + 30 * np.random.random((N_trajectories, 3))

# Solve for the trajectories
x_t = np.array([
    euler.euler3D( 2000, .002, xi, euler.lorentz_deriv)
    for xi in x0
])

# Set up figure & 3D axis for animation
fig = plt.figure()
ax = fig.add_axes([0, 0, 1, 1], projection='3d')
ax.axis('off')

# choose a different color for each trajectory
colors = plt.cm.jet(np.linspace(0, 1, N_trajectories))

# set up lines and points
lines = sum([ax.plot([], [], [], '-', c=c) for c in colors], [])
pts = sum([ax.plot([], [], [], 'o', c=c) for c in colors], [])

# prepare the axes limits
ax.set_xlim((-25, 25))
ax.set_ylim((-35, 35))
ax.set_zlim((5, 55))

# set point-of-view: specified by (altitude degrees, azimuth degrees)
ax.view_init(30, 0)

# initialization function: plot the background of each frame
def init():
    for line, pt in zip(lines, pts):
        line.set_data([], [])
        line.set_3d_properties([])

        pt.set_data([], [])
        pt.set_3d_properties([])
    return lines + pts

# animation function.  This will be called sequentially with the frame number
def animate(i):
    # reset the animation whenever it gets past the last frame
    i = i % x_t.shape[1]

    for line, pt, xi in zip(lines, pts, x_t):
        x, y, z = xi[:i].T
        line.set_data(x, y)
        line.set_3d_properties(z)

        pt.set_data(x[-1:], y[-1:])
        pt.set_3d_properties(z[-1:])
    ax.view_init(elev=30, azim=.3 * i)
    fig.canvas.draw()
    return lines + pts

# instantiate the animator
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=1000, interval=15, blit=False)
plt.ioff()
plt.show()
#     if writeout:
#         mywriter = animation.FFMpegWriter(bitrate=4000)                                                                                # you have to install FFMpeg if you want to write out to mp4
#         anim.save(str(N_trajectories)+'_trajectories_4x_n='+str(n)+'largersteps.mp4', writer='ffmpeg', fps=60, extra_args=['-vcodec', 'libx264']) # autogenerate filenames and export
#         print("saved the file!")
#         print("savetime is", time.time()-start_time)
#     plt.close()
#     print('combined runtime is', time.time() - first_time)
