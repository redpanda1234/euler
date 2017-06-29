import time                                       # for sleep and keeping track of runtimes
import numpy as np                                # numpy!

from matplotlib import pyplot as plt              # for animation
from mpl_toolkits.mplot3d import Axes3D           # ibid
from matplotlib.colors import cnames              # ibid
from matplotlib import animation                  # ibid
import backend                                    # import your own simulation function HERE!

# initialization function: plot the background of each frame
def init():
    for line, pt in zip(lines, pts): # iterate through all line-pt pairs
        line.set_data([], [])        # clear entries/data in prep for sim (get shape right)
        line.set_3d_properties([])

        pt.set_data([], [])
        pt.set_3d_properties([])
    return lines + pts

# animation function.  This will be called sequentially with the frame number
def animate(frame_num):
    steps_per_frame = 300                                     # number of timesteps to jump when we advance frames
    frame_index = (steps_per_frame * frame_num) % x_t.shape[1]# x_t.shape[1] gives the total number of timesteps. Modding allows us to reset the anim once it reaches the end of the timesteps.
    for line, pt, xi in zip(lines, pts, x_t):                 # iterates through all trajectories by matching them to a line and point at some time step
        x, y, z = xi[:frame_index].T                          # gets all pounts in the line so far.  Transpose needed bc numpy stores pos as column vecs.
        line.set_data(x, y)                                   # add the (x,y) coordinates of all points comprising the line
        line.set_3d_properties(z)                             # same but for z
        pt.set_data(x[-1:], y[-1:])                           # get the final point in the line, so that we can draw the object (point) there
        pt.set_3d_properties(z[-1:])                          #
    ax.view_init(30, 0.001 * frame_index)                     #
    fig.canvas.draw()                                         #
    return lines + pts

def wrapper(r_exp_list, N_trajectories, writeout):
    print("called wrapper")                                   # not Dr. Dre, sadly.  I wish I had him on dial.
    first_time = time.time()                                  # because I have lots of other "start_time" defninitons sprinkled throughout
    for n in r_exp_list:                                      # iterate through a list of exponent values for r in newton's law of gravitation
        print("current job: r**(-", n,")")                    # when runtimes get long it's nice to know how far through you are
        np.random.seed(1)
        x0 = -2 + 4 * np.random.random((N_trajectories, 3))   # randomizes starting position for each trajectory
        v0 = -1 + 2 * np.random.random((N_trajectories, 3))   # randomizes starting velocity for each trajectory
        p0 = zip(x0,v0)                                       # iterates through and returns x0 and v0 pairs in one tuple, p0.  For ease in the list comprehension below.
        global x_t                                            # so that the animate function can still use this
        x_t = np.asarray([backend.simulate(pi[0],pi[1],1,1,n,.0001,120000) for pi in p0]) # if you're outputting from your own function, make sure that it's an array of position vectors (also arrays!)
        print(x_t)
        num_traj = 0
        for traj in x_t:
            num_traj+=1
            text_file = open("Output_for"+str(num_traj)+str(n)+".txt", "w")
            text_file.write(str(traj)+"\n\n\n\n\n\n")
            text_file.close()
        # Set up figure & 3D axis for animation
        global fig                                            #
        fig = plt.figure()                                    #
        global ax                                             #
        ax = fig.add_axes([0, 0, 1, 1], projection='3d')      #
        ax.axis('on')                                         # sets the background axes "on".  Change to "off" if you want a more artistic/minimalistic viewing experience

        # choose a different color for each trajectory
        global colors
        colors = plt.cm.jet(np.linspace(0, 1, N_trajectories))

        # set up lines and points
        global lines
        lines = sum([ax.plot([], [], [], '-', c=c) for c in colors], [])
        global pts
        pts = sum([ax.plot([], [], [], 'o', c=c) for c in colors], [])

        # prepare the axes limits
        ax.set_xlim((-15, 15))
        ax.set_ylim((-15, 15))
        ax.set_zlim((-5, 5))

        # set point-of-view: specified by (altitude degrees, azimuth degrees)
        ax.view_init(30, 0)
        # instantiate the animator.
        start_time = time.time()
        anim = animation.FuncAnimation(fig, animate, init_func=init, frames=4000, interval=30, blit=True)
        print("anim_time is", time.time()-start_time)
        start_time = time.time()
        plt.show()
        if writeout:
            mywriter = animation.FFMpegWriter(bitrate=4000)                                                                                # you have to install FFMpeg if you want to write out to mp4
            anim.save(str(N_trajectories)+'_trajectories_4x_n='+str(n)+'largersteps.mp4', writer='ffmpeg', fps=60, extra_args=['-vcodec', 'libx264']) # autogenerate filenames and export
            print("saved the file!")
            print("savetime is", time.time()-start_time)
        plt.close()
    print('combined runtime is', time.time() - first_time)
wrapper([2], 10, False)
