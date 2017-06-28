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

from helpers import *

from camera import Camera
from tk_scene import TkSceneRoot

# For path joining
import os

# GGOTTA GO FASTTTTT
import numpy as np


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

# The density of points in point-cloud mobjects.
DEFAULT_POINT_DENSITY_2D = 25
DEFAULT_POINT_DENSITY_1D = 250

# point thickness for point-cloud mobjects
DEFAULT_POINT_THICKNESS = 2

# float parameter for height/width of the space
#TODO, Make sure these are not needed
SPACE_HEIGHT = 8.0
# define a float value for space width in terms of aspect ratio
SPACE_WIDTH = SPACE_HEIGHT * DEFAULT_WIDTH / DEFAULT_HEIGHT

# Space buffer between mobjects
SMALL_BUFF = 0.1
MED_SMALL_BUFF = 0.25
MED_LARGE_BUFF = 0.5
LARGE_BUFF = 1

#
DEFAULT_MOBJECT_TO_EDGE_BUFFER = MED_LARGE_BUFF
DEFAULT_MOBJECT_TO_MOBJECT_BUFFER = MED_SMALL_BUFF

#All in seconds
DEFAULT_ANIMATION_RUN_TIME = 1.0
DEFAULT_POINTWISE_FUNCTION_RUN_TIME = 3.0
DEFAULT_DITHER_TIME = 1.0


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


### Colors ###


COLOR_MAP = {
    "DARK_BLUE"   : "#236B8E",
    "DARK_BROWN"  : "#8B4513",
    "LIGHT_BROWN" : "#CD853F",
    "BLUE_E"      : "#1C758A",
    "BLUE_D"      : "#29ABCA",
    "BLUE_C"      : "#58C4DD",
    "BLUE_B"      : "#9CDCEB",
    "BLUE_A"      : "#C7E9F1",
    "TEAL_E"      : "#49A88F",
    "TEAL_D"      : "#55C1A7",
    "TEAL_C"      : "#5CD0B3",
    "TEAL_B"      : "#76DDC0",
    "TEAL_A"      : "#ACEAD7",
    "GREEN_E"     : "#699C52",
    "GREEN_D"     : "#77B05D",
    "GREEN_C"     : "#83C167",
    "GREEN_B"     : "#A6CF8C",
    "GREEN_A"     : "#C9E2AE",
    "YELLOW_E"    : "#E8C11C",
    "YELLOW_D"    : "#F4D345",
    "YELLOW_C"    : "#FFFF00",
    "YELLOW_B"    : "#FFEA94",
    "YELLOW_A"    : "#FFF1B6",
    "GOLD_E"      : "#C78D46",
    "GOLD_D"      : "#E1A158",
    "GOLD_C"      : "#F0AC5F",
    "GOLD_B"      : "#F9B775",
    "GOLD_A"      : "#F7C797",
    "RED_E"       : "#CF5044",
    "RED_D"       : "#E65A4C",
    "RED_C"       : "#FC6255",
    "RED_B"       : "#FF8080",
    "RED_A"       : "#F7A1A3",
    "MAROON_E"    : "#94424F",
    "MAROON_D"    : "#A24D61",
    "MAROON_C"    : "#C55F73",
    "MAROON_B"    : "#EC92AB",
    "MAROON_A"    : "#ECABC1",
    "PURPLE_E"    : "#644172",
    "PURPLE_D"    : "#715582",
    "PURPLE_C"    : "#9A72AC",
    "PURPLE_B"    : "#B189C6",
    "PURPLE_A"    : "#CAA3E8",
    "WHITE"       : "#FFFFFF",
    "BLACK"       : "#000000",
    "LIGHT_GRAY"  : "#BBBBBB",
    "LIGHT_GREY"  : "#BBBBBB",
    "GRAY"        : "#888888",
    "GREY"        : "#888888",
    "DARK_GREY"   : "#444444",
    "DARK_GRAY"   : "#444444",
    "GREY_BROWN"  : "#736357",
    "PINK"        : "#D147BD",
    "GREEN_SCREEN": "#00FF00",
    "ORANGE"      : "#FF862F",
}
#####
PALETTE = COLOR_MAP.values()        # Set the color palette we can choose from
locals().update(COLOR_MAP)          # Update the local symbol table to add our colors
for name in filter(lambda s : s.endswith("_C"), COLOR_MAP.keys()): #For all colors ending in _C,
    locals()[name.replace("_C", "")] = locals()[name] # I'm not sure what this is doing.
                                                      # shouldn't the order of these two sides be
                                                      # switched??


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
