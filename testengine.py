from PIL import Image
from colour import Color
import numpy as np
import itertools as it
import warnings
import time
import os
import copy
from tqdm import tqdm as ProgressDisplay
import inspect
import subprocess as sp

from tk_scene import TkSceneRoot

# For path joining
import os

# GGOTTA GO FASTTTTT
import numpy as np

from scipy import integrate
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import cnames
from matplotlib import animation



# Set default animation resolution
DEFAULT_HEIGHT = 2160
DEFAULT_WIDTH  = 3840

# Set FPS
LOW_QUALITY_FRAME_DURATION = 1./20
MEDIUM_QUALITY_FRAME_DURATION = 1./30
PRODUCTION_QUALITY_FRAME_DURATION = 1./60
# For all you MLG's out there ;)
SUPER_QUALITY_FRAME_DURATION = 1./144

# There might be other configuration than pixel_shape later...
# Set the resolution of the final output animation
PRODUCTION_QUALITY_CAMERA_CONFIG = {
    "pixel_shape" : (DEFAULT_HEIGHT, DEFAULT_WIDTH),
}

# Describes the dimensions for medium quality resolution
MEDIUM_QUALITY_CAMERA_CONFIG = {
    "pixel_shape" : (720, 1280),
}

# Same, but for low quality
LOW_QUALITY_CAMERA_CONFIG = {
    "pixel_shape" : (480, 853),
}

# float parameter for height/width of the space
#TODO, Make sure these are not needed
SPACE_HEIGHT = 8.0
# define a float value for space width in terms of aspect ratio
SPACE_WIDTH = SPACE_HEIGHT * DEFAULT_WIDTH / DEFAULT_HEIGHT

# Set the coordinates of the origin in our animation space, and also define a basis
ORIGIN = np.array(( 0, 0, 0))
UP     = np.array(( 0, 1, 0))
DOWN   = np.array(( 0,-1, 0))
RIGHT  = np.array(( 1, 0, 0))
LEFT   = np.array((-1, 0, 0))
OUT    = np.array(( 0, 0, 1))
IN     = np.array(( 0, 0,-1))

# Defines the directioned top of the animation frame
TOP        = SPACE_HEIGHT*UP
BOTTOM     = SPACE_HEIGHT*DOWN
LEFT_SIDE  = SPACE_WIDTH*LEFT
RIGHT_SIDE = SPACE_WIDTH*RIGHT

# Obtain the current path name for use in creating new files
# That way we can append the current path to the relative generated path
THIS_DIR          = os.path.dirname(os.path.realpath(__file__))
FILE_DIR          = os.path.join(THIS_DIR, "files")         # Dir for project files
IMAGE_DIR         = os.path.join(FILE_DIR, "images")        # Project images
GIF_DIR           = os.path.join(FILE_DIR, "gifs")          # Etc. for gif
MOVIE_DIR         = os.path.join(FILE_DIR, "movies")
STAGED_SCENES_DIR = os.path.join(FILE_DIR, "staged_scenes")
TEX_DIR           = os.path.join(FILE_DIR, "Tex")           # For LaTeX annotations
TEX_IMAGE_DIR     = os.path.join(IMAGE_DIR, "Tex")          # Make subdir for TeX in images
MOBJECT_DIR       = os.path.join(FILE_DIR, "mobjects")
IMAGE_MOBJECT_DIR = os.path.join(MOBJECT_DIR, "image")

for folder in [FILE_DIR, IMAGE_DIR, GIF_DIR, MOVIE_DIR, TEX_DIR,
               TEX_IMAGE_DIR, MOBJECT_DIR, IMAGE_MOBJECT_DIR,
               STAGED_SCENES_DIR]:
    if not os.path.exists(folder):     # check if the directories above exist
        os.mkdir(folder)               # if not... no problem!  Make one.


FFMPEG_BIN = "ffmpeg"  # Binary for ffmpeg

class Scene(object):
    CONFIG = {
        "camera_class"     : Camera,
        "camera_config"    : {},
        "frame_duration"   : LOW_QUALITY_FRAME_DURATION,
        "construct_args"   : [],
        "skip_animations"  : False,
        "write_to_movie"   : False,
        "save_frames"      : False,
        "output_directory" : MOVIE_DIR,
        "name" : None,
    }
    def __init__(self, **kwargs):
        self.saved_frames = []
        self.shared_locals = {}
        if self.name is None:
            self.name = self.__class__.__name__

        self.setup()
        if self.write_to_movie:
            self.open_movie_pipe()
        self.construct(*self.construct_args)
        if self.write_to_movie:
            self.close_movie_pipe()

    def get_movie_file_path(self, name, extension):
        file_path = os.path.join(self.output_directory, name)
        if not file_path.endswith(extension):
            file_path += extension
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)
        return file_path

    def open_movie_pipe(self):
        name = str(self)
        file_path = self.get_movie_file_path(name, ".mp4")
        temp_file_path = file_path.replace(".mp4", "Temp.mp4")
        print "Writing to %s"%temp_file_path
        self.args_to_rename_file = (temp_file_path, file_path)

        fps = int(1/self.frame_duration)
        height, width = self.camera.pixel_shape

        command = [
            FFMPEG_BIN,
            '-y',                 # overwrite output file if it exists
            '-f', 'rawvideo',
            '-vcodec','rawvideo',
            '-s', '%dx%d'%(width, height), # size of one frame
            '-pix_fmt', 'rgb24',
            '-r', str(fps), # frames per second
            '-i', '-',      # The imput comes from a pipe
            '-an',          # Tells FFMPEG not to expect any audio
            '-vcodec', 'mpeg',
            '-c:v', 'libx264',
            '-pix_fmt', 'yuv420p',
            '-loglevel', 'error',
            temp_file_path,
        ]
        self.writing_process = sp.Popen(command, stdin=sp.PIPE)

    def close_movie_pipe(self):
        self.writing_process.stdin.close()
        self.writing_process.wait()
        os.rename(*self.args_to_rename_file)

class Test(Scene):
    N_trajectories = 20

    def lorentz_deriv(self, pos, t0, sigma=10., beta=8./3, rho=28.0):
        """Compute the time-derivative of a Lorentz system."""
        x, y, z = pos[0], pos[1], pos[2]
        return [sigma * (y - x), x * (rho - z) - y, x * y - beta * z]

    # Choose random starting points, uniformly distributed from -15 to 15
    np.random.seed(1)
    x0 = -15 + 30 * np.random.random((N_trajectories, 3))

    # Solve for the trajectories
    t = np.linspace(0, 4, 1000)
    x_t = np.asarray([integrate.odeint(lorentz_deriv, x0i, t)
                      for x0i in x0])

    # Set up figure & 3D axis for animation
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1], projection='3d')
    ax.axis('off')

    # choose a different color for each trajectory
    colors = plt.cm.jet(np.linspace(0, 1, N_trajectories))

    # set up lines and points
    lines = sum([ax.plot([], [], [], '-', c=c)
                 for c in colors], [])
    pts = sum([ax.plot([], [], [], 'o', c=c)
               for c in colors], [])

    # prepare the axes limits
    ax.set_xlim((-25, 25))
    ax.set_ylim((-35, 35))
    ax.set_zlim((5, 55))

    # set point-of-view: specified by (altitude degrees, azimuth degrees)
    ax.view_init(30, 0)

    # initialization function: plot the background of each frame
    def init(self):
        for line, pt in zip(lines, pts):
            line.set_data([], [])
            line.set_3d_properties([])

            pt.set_data([], [])
            pt.set_3d_properties([])
            return lines + pts


    # animation function.  This will be called sequentially with the frame number
    def animate(self, i):
        # we'll step two time-steps per frame.  This leads to nice results.
        i = (2 * i) % x_t.shape[1]

        for line, pt, xi in zip(lines, pts, x_t):
            x, y, z = xi[:i].T
            line.set_data(x, y)
            line.set_3d_properties(z)

            pt.set_data(x[-1:], y[-1:])
            pt.set_3d_properties(z[-1:])

            ax.view_init(30, 0.3 * i)
            fig.canvas.draw()
            return lines + pts

        # instantiate the animator.
        anim = animation.FuncAnimation(fig, animate, init_func=init,
                                       frames=1000, interval=30, blit=True)

        # Save as mp4. This requires mplayer or ffmpeg to be installed
        anim.save('lorentz_attractor.mp4', fps=60, extra_args=['-vcodec', 'libx264'])

        plt.show()
