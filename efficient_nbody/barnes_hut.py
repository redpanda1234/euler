import numpy as np
import time
import math
import os
import subprocess
import progressbar
import sys

# for parallel processing
from joblib import Parallel, delayed
import multiprocessing


# for drawing out resulting frames
from PIL import Image, ImageDraw

# get numpy to actually throw errors, instead of just printing them.
np.seterr(all='raise')

# threshold s/d value for determining whether to recurse into tree
theta = 0.5

# because I'm dumb
sys.setrecursionlimit(500)

class BoundRegion:
    """
    BoundRegion class represents a square on the grid we're simulating over.
    """
    def __init__(self, corners):
        """
        Takes as input an array/tuple of 4 numpy arrays containing the (x,y) pairs
        of corners.
        """
        # define the corners
        self.NE_corner, self.NW_corner, self.SW_corner, self.SE_corner = corners

        # define the midpoints of the sides
        self.N = .5 * (self.NE_corner + self.NW_corner)
        self.W = .5 * (self.NW_corner + self.SW_corner)
        self.S = .5 * (self.SW_corner + self.SE_corner)
        self.E = .5 * (self.SE_corner + self.NE_corner)

        # get the center of the square
        self.center = .25 * (self.N + self.W + self.S + self.E)

        # store the square sidelength as an attribute
        self.sidelength = (self.NE_corner[0] - self.NW_corner[0])

    def contains(self, point):
        """
        This method takes as input an array defining a point, and checks if the
        point is within the borders of the region.  Returns bool.
        """
        x,y = point # get the x and y coodinates out of the point array
        # similarly, use the splat operator * to unpack the x,y for corners
        lower_x, lower_y, upper_x, upper_y = [*self.SW_corner, *self.NE_corner]
        if lower_x <= x and x <= upper_x: # check if x in bounds
            if lower_y <= y and y <= upper_y: # and check if y in bounds
                return True
        return False

    def get_NE(self):
        """
        This method returns a sub-region of the calling region, corresponding
        to the north-east quadrant (quadrant I)
        """
        return BoundRegion( ( ( self.NE_corner, self.N, self.center, self.E ) ) )

    def get_NW(self):
        """
        This method returns a sub-region of the calling region, corresponding
        to the north-west quadrant (quadrant II)
        """
        return BoundRegion( ( ( self.N, self.NW_corner, self.W, self.center ) ) )

    def get_SW(self):
        """
        This method returns a sub-region of the calling region, corresponding
        to the south-west quadrant (quadrant III)
        """
        return BoundRegion( ( ( self.center, self.W, self.SW_corner, self.S ) ) )

    def get_SE(self):
        """
        This method returns a sub-region of the calling region, corresponding
        to the south-east quadrant (quadrant IV)
        """
        return BoundRegion( ( ( self.E, self.center, self.S, self.SE_corner ) ) )

    def draw(self, canvas):
        """
        ToDo
        """

        pass

class Body:
    """
    Class body.  Can either be a single particle or correspond to a collection
    of particles clustered as a single object (for reference as nodes by the
    tree structure)
    """
    def __init__(
            self,
            m_array = np.array([0]),
            pos_array = np.array([[0,0]]),
            v_array = np.array([0.,0.]),
            f_array = np.array([0.,0.]),
            sub_bodies = [],
            RGB_tuple = (245,245,245)
    ):
        """
        Body takes as input a 1 x n array of mass values, a n x 2 array of the
        corresponding positions of said masses, a 1x2 array corresponding to the
        velocity vector of the center of mass of the body, a 1x2 array similarly
        corresponding to the force acting on the center of mass, and an array of
        sub_bodies.
        """
        self.m_array = m_array # store discrete masses as an attribute in array
        self.pos_array = pos_array # similarly with positions

        self.sub_bodies = sub_bodies
        if self.sub_bodies:
            self.vel = v_array
        else:
            self.vel = v_array[0]
        self.frc = f_array

        self.mass = self.get_mass()
        if self.mass != 0:
            self.pos = self.get_CoM() # define position as center of mass
        else:
            self.pos = np.array([0,0])

        self.RGB_tuple = RGB_tuple

    def __repr__(self):
        str_out = "\n"
        str_out += "Mass array:" + str( self.m_array ) + "\n"
        str_out += "Position array:" + str( self.pos_array ) + "\n"
        str_out += "Velocity array:" + str(self.vel) + "\n"
        str_out += "Force on object:" + str(self.frc) + "\n"
        str_out += "Sub-bodies contained:" + str( self.sub_bodies ) + "\n"
        str_out += "Total mass:" + str(self.mass) + "\n"
        str_out += "Center of mass of Body:" + str( self.pos )
        return str_out

    def get_mass(self):
        """
        This method iterates through all the constituent bodies in Body, and
        returns the total mass.
        """
        total_mass = 0
        for mass in self.m_array:
            total_mass += mass
        return total_mass

    def get_CoM(self):
        """
        Ok this is really cool: center of mass equation is essentially the
        inner product of a mass vector and a matrix of position vectors!

        if mass vector is row vector (which it should be), transpose it.

        This method takes advantage of that, and uses it to quickly calculate
        the center of mass of the array without
        """
        transposed_mass_array = self.m_array.T # transpose the mass array
        return (np.dot( transposed_mass_array, self.pos_array ))/self.mass


    def update(self, dt):
        """
        This method uses Euler's method to update position and velocity
        of the body over a small time interval dt
        """
        #print("updating!")
        #print(self.vel, self.pos)
        #print(self.vel, self.pos)
        self.vel += dt * self.frc / self.mass
        self.pos += dt * self.vel
        #print(self.vel, self.pos)
        #print(self.vel, self.pos)

    def distance_to(self, other_body):
        """
        This method returns a tuple of the displacement in x and y between
        the calling body (self) and the second body (other_body)
        """
        return np.array([self.pos[0]-other_body.pos[0], self.pos[1]-other_body.pos[1]])

    def in_region(self, region):
        """
        Checks if the body is contained in the passed region
        """
        return region.contains(self.pos)


    def sum(self, other_body):
        """
        This method merges the calling body and other_body into
        a single object of type body, and returns it.
        """
        m_array = np.append(self.m_array, other_body.m_array)
        pos_array = np.append(self.pos_array, other_body.pos_array, axis=0)
        #print("summing")
        #print(m_array, pos_array)
        return Body(m_array, pos_array)

    def reset(self):
        """
        resets the force array to 0 so that forces don't pile up over
        timesteps.
        """
        self.frc = np.array([0,0])

    def draw(self, draw):
        """
        ToDo
        """
        pass


class Quadtree:

    def __init__(self, region, bodies, empty=False):
        """
        Quadtree creates an object to store the Barnes-hut tree for the n-body
        simulator.  Each node corresponds to an object of type Quadtree and its
        corresponding region and body.  Recursive generation stops when a region
        contains either 0 or 1 bodies.
        """
        self.region = region # store reference to region in node
        self.NE = self.region.get_NE() # recursively get subregions
        self.NW = self.region.get_NW()
        self.SW = self.region.get_SW()
        self.SE = self.region.get_SE()

        self.bodies = bodies
        if bodies:
            self.body = bodies[0]
        self.NE_bodies = [body for body in self.bodies if body.in_region(self.NE)]
        self.NW_bodies = [body for body in self.bodies if body.in_region(self.NW)]
        self.SW_bodies = [body for body in self.bodies if body.in_region(self.SW)]
        self.SE_bodies = [body for body in self.bodies if body.in_region(self.SE)]

        if len(self.bodies) > 1:
            #print("constructing subtrees")
            self.subtrees = [
                Quadtree(self.NE, self.NE_bodies),
                Quadtree(self.NW, self.NW_bodies),
                Quadtree(self.SW, self.SW_bodies),
                Quadtree(self.SE, self.SE_bodies)
            ]
        else:
            self.subtrees = []

    def insert(self, body):
        """
        Inserts body into the mass array for the node, and updates the center of
        mass accordingly.  Regenerates the corresponding subregion tree if
        necessary
        """
        if body not in self.bodies:
            self.bodies += [body]
            if len(self.bodies) > 1:
                if body.in_region(self.NE):
                    self.NE_bodies += [body]
                    self.BH_NE = Quadtree(self.NE, self.NE_bodies)
                    self.subtrees[0] = self.BH_NE
                elif body.in_region(self.NW):
                    self.NW_bodies += [body]
                    self.BH_NW = Quadtree(self.NW, self.NW_bodies)
                    self.subtrees[1] = self.BH_NW
                elif body.in_region(self.SW):
                    self.SW_bodies += [body]
                    self.BH_SW = Quadtree(self.SW, self.SW_bodies)
                    self.subtrees[2] = self.BH_SW
                elif body.in_region(self.SE):
                    self.SE_bodies += [body]
                    self.BH_SE = Quadtree(self.SE, self.SE_bodies)
                    self.subtrees[3] = self.BH_SE
                else:
                    pass
        try:
            self.body = self.body.sum(body)
        except AttributeError:
            self.body = body

    def check_bodies(self):
        """
        """
        for i in range( len( self.bodies ) - 1 ):
            for j in range( i+1, len( self.bodies ) + 1 ):
                try:
                    if np.array_equal(self.bodies[i].pos, self.bodies[j].pos):
                        self.bodies[i] = self.bodies[i].sum(self.bodies[j])
                        self.bodies = self.bodies[:j] + self.bodies[j+1:]
                        j -= 1
                except IndexError:
                    pass


    def isFar(self, body):
        """
        Calculates metric for determining whether or not to transverse the quadtree
        further when calculating force.
        """
        global theta
        s = self.region.sidelength
        d = np.linalg.norm(self.body.distance_to(body))
        return ( ( s/d ) < theta )

    def get_force(self, body):
        """
        Calculate the force that self exerts on body.  If the calling object
        is a single particle, use simple newton's law.  Else, if it's sufficiently
        far away, treat self like a cluster of particles stored at their center of
        mass. If it's not, then recurse into the subtree structure and repeat.
        """
        if hasattr(self, "body"):

            if len(self.bodies) == 1 and self.body != body:
                distance_array = body.distance_to(self.body)
                distance = np.linalg.norm(distance_array)
                numerator = ( -6.67 * ( 10 ** ( -11 ) ) * self.body.mass * body.mass)
                net_force = numerator / (distance**2)
                body.frc += np.array([net_force * distance_array[0]/distance, net_force * distance_array[1]/distance])
            elif self.body == body:
                return
            else:
                if self.isFar(body):
                    distance_array = body.distance_to(self.body)
                    distance = np.linalg.norm(distance_array)
                    numerator = (-6.67 * ( 10** ( -11 ) ) * self.body.mass * body.mass)
                    net_force = numerator / (distance**2)
                    body.frc += np.array([net_force * distance_array[0]/distance, net_force * distance_array[1]/distance])
                else:
                    if hasattr(self, 'subtrees'):
                        for subtree in self.subtrees:
                            subtree.get_force(body)

class System:
    """
    Overall wrapper
    """
    def __init__(self, max_t, dt, corners, m_list, im_width=2000, threshold = .1):
        """
        masses should be passed as np arrays of [mass, [x,y], [vx,vy] ]
        """
        self.max_t = max_t
        self.dt = dt

        self.im_width = im_width

        self.m_list = m_list
        self.threshold = threshold
        self.space = BoundRegion(corners)
        self.NW = corners[1]

        body_list = []
        for mass in self.m_list:
            body = Body(m_array = np.array(mass[0]), pos_array = np.array(mass[1]), v_array = np.array(mass[2]), RGB_tuple = mass[3])
            body_list.append(body)

        self.masterTree = Quadtree(self.space, body_list)
        for body in self.masterTree.bodies:
            self.masterTree.insert(body)

    def start(self):
        if type(self.dt) == int:
            bar = progressbar.ProgressBar()
            for time in bar(range(0, self.max_t, self.dt)):
                #print("\ntimestep:", time/self.dt, "of", self.max_t/self.dt)
                self.update('{:0>8}'.format( str( int(time/self.dt) ) ) + ".png" )
        elif type(self.dt) == float:
            img_num = 0
            bar = progressbar.ProgressBar()
            for time in bar(np.linspace(0,self.max_t, self.max_t/self.dt)):
                self.update('{:0>8}'.format( str( img_num ) ) + ".png" )
                img_num += 1
        else:
            raise TypeError("dt must be int or float.  Got" + str(type(self.dt)) + "instead.")

    def to_pixel(self, pos, width, sidelength):
        """
        pos should be numpy array, width should be pixel length of picture, e.g. 2000,
        sidelength should be sidelength of the space.
        """
        width -= 1 # off-by-one error
        if self.space.contains(pos):
            rel_pos = pos - self.NW #self.NW is (0,0) in PIL
            rel_pos[1] = -1*rel_pos[1] # flip the sign
            rel_pos = rel_pos/sidelength
            rel_pos *= width
            rel_pos = np.rint(rel_pos).astype(int)
            rel_pos = rel_pos.tolist()
            return rel_pos

    def draw_boxes(self, tree, draw):
        """
        draw is an object of type PIL.ImageDraw.Draw
        """
        if hasattr(tree, "subtrees"):
            for subtree in tree.subtrees:
                self.draw_boxes(subtree, draw)

        corner_1 = self.to_pixel(tree.region.NW_corner, self.im_width, self.space.sidelength)
        corner_2 = self.to_pixel(tree.region.SE_corner, self.im_width, self.space.sidelength)
        draw.rectangle(np.append(corner_1, corner_2).tolist(), outline=(0,255,0))


    def update(self, filename):
        """

        """
        time.sleep(5)
        canvas = Image.new("RGB", (self.im_width, self.im_width))
        draw = ImageDraw.Draw(canvas)
        canvas2 = Image.new("RGB", (self.im_width, self.im_width))
        draw2 = ImageDraw.Draw(canvas2)
        self.masterTree = Quadtree(self.space, self.masterTree.bodies)
        for body in self.masterTree.bodies:
            self.masterTree.insert(body)
            try:
                draw.point( self.to_pixel( body.pos, self.im_width, self.space.sidelength), fill = body.RGB_tuple)
                draw2.point( self.to_pixel( body.pos, self.im_width, self.space.sidelength), fill = body.RGB_tuple)
            except TypeError:
                pass
        for body in self.masterTree.bodies:
            #print(self.masterTree.bodies)
            #print(self.space.contains(body.pos))
            self.masterTree.get_force(body)
            body.update(self.dt)
        self.draw_boxes(self.masterTree, draw)
        canvas.save("boxed_"+filename, format="PNG")
        canvas2.save(filename, format="PNG")

def wrapper(filename, max_t = 10000000, dt = 25000, im_width = 2000):
    """
    Takes as input a string corresponding to the name of a file in ./rawdata/
    and sets the parameters for the system.
    """
    home_dir = os.getcwd()
    os.chdir("raw_data")
    file = open(filename, "r")
    data = file.read()
    data_list = data.split( "\n" )
    radius = float(data_list[1])
    m_list = []
    for star in data_list[2:]:
        if star:
            star = star.split(" ")
            star = [char for char in star if len(char) != 0]
            for i in range(5):
                star[i] = float(star[i])
            for i in range(5,8):
                star[i] = int(star[i])
            m_list += [ [ np.array( [ star[4] ] ), np.array( [ [ star[0], star[1] ] ] ), np.array( [ [ star[2], star[3] ] ] ), ( star[5], star[6], star[7] ) ] ]
    os.chdir("..")
    if not os.path.exists("tests"):
        os.mkdir("tests")
    os.chdir("tests")
    if not os.path.exists(filename):
        os.mkdir(filename)
    else:
        delete = input("dir \"./tests/" + str(filename) + "/\" already exists.  Remove it? Enter yes to confirm, and any other char will cancel it.")
        if delete == "yes":
            subprocess.run(["rm", "-rf", filename+"/"])
            os.mkdir(filename)
        else:
            return
    os.chdir(filename)
    corners = [ np.array([radius, radius]), np.array([-radius, radius]), np.array([-radius, -radius]), np.array([radius, -radius]) ]
    simulation = System(max_t, dt, corners, m_list, im_width = im_width)
    simulation.start()
    write_command = [
        "ffmpeg", # use ffmpeg to convert output images to vide
        "-r", "60", # set fps to 60
        "-f", "image2", # input format (is this necessary?)
        "-s", str(im_width) + "x" + str(im_width), # set output resolution
        "-i", "%08d.png", # how to find the file.  %08d.png tells ffmpeg the string will be padded w/ 8 zeros
        "-vcodec", "libx264",
        "-crf", "25", # rate factor.  Sets output quality/speed. 18-25 good.
        "-pix_fmt", "yuv420p", # input pixel format
        filename + ".mp4"
    ]
    subprocess.run(write_command)
    write_command_2 = [
        "ffmpeg", # use ffmpeg to convert output images to vide
        "-r", "60", # set fps to 60
        "-f", "image2", # input format (is this necessary?)
        "-s", str(im_width) + "x" + str(im_width), # set output resolution
        "-i", "boxed_%08d.png", # how to find the file.  %08d.png tells ffmpeg the string will be padded w/ 8 zeros
        "-vcodec", "libx264",
        "-crf", "25", # rate factor.  Sets output quality/speed. 18-25 good.
        "-pix_fmt", "yuv420p", # input pixel format
        "boxed_"+filename + ".mp4"
    ]
    subprocess.run(write_command2)
    os.chdir(home_dir)

    #Current issues: self.body.mass for the system is broken.
    # once you have an imagewriting matpolotlib
    # parallel wrapping of loop
