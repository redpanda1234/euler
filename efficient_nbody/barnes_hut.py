import numpy as np
import time
import math
import os
import subprocess
import progressbar
import sys

# for drawing out resulting frames
from PIL import Image, ImageDraw

# get numpy to actually throw errors, instead of just printing them.
np.seterr(all='raise')

# threshold s/d value for determining whether to recurse into tree
theta = 0.5

# because I'm dumb
sys.setrecursionlimit(1500)

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

    def draw(self):
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
            v_array = np.array([0,0]),
            f_array = np.array([0,0]),
            sub_bodies = []
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
            self.pos = None

    def __repr__(self):
        str_out = ""
        str_out += "Object of type body.\n\n"
        str_out += "Mass array:" + str( self.m_array ) + "\n"
        str_out += "Position array:" + str( self.pos_array ) + "\n"
        str_out += "Velocity array:" + str(self.vel) + "\n"
        str_out += "Force on object:" + str(self.frc) + "\n"
        str_out += "Sub-bodies contained:" + str( self.sub_bodies ) + "\n"
        str_out += "Total mass:" + str(self.mass) + "\n"
        str_out += "Center of mass of Body:" + str( self.pos ) + "\n"
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
        self.vel += dt * self.frc / self.mass
        #print(self.pos, self.vel)
        self.pos += dt * self.vel

    def distance_to(self, other_body):
        """
        This method returns a tuple of the displacement in x and y between
        the calling body (self) and the second body (other_body)
        """
        return (self.pos[0]-other_body.pos[0], self.pos[1]-other_body.pos[1])

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
        return Body(m_array, pos_array)

    def reset(self):
        """
        resets the force array to 0 so that forces don't pile up over
        timesteps.
        """
        self.frc = np.array([0,0])

    def draw(self, canvas):
        """
        ToDo
        """
        pass


class Quadtree:

    def __init__(self, region, bodies = [], debug=False):
        """
        Quadtree creates an object to store the Barnes-hut tree for the n-body
        simulator.  Each node corresponds to an object of type Quadtree and its
        corresponding region and body.  Recursive generation stops when a region
        contains either 0 or 1 bodies.
        """
        self.region = region # store reference to region in node
        self.bodies = bodies #

        self.NE = self.region.get_NE()
        self.NW = self.region.get_NW()
        self.SW = self.region.get_SW()
        self.SE = self.region.get_SE()

        self.NE_bodies = [body for body in self.bodies if body.in_region(self.NE)]
        self.NW_bodies = [body for body in self.bodies if body.in_region(self.NW)]
        self.SW_bodies = [body for body in self.bodies if body.in_region(self.SW)]
        self.SE_bodies = [body for body in self.bodies if body.in_region(self.SE)]

        subtrees = []

        if len(bodies) > 1:
            if self.NE_bodies:
                self.BH_NE = Quadtree(self.NE, self.NE_bodies)
                subtrees += [self.BH_NE]
            if self.NW_bodies:
                self.BH_NW = Quadtree(self.NW, self.NW_bodies)
                subtrees += [self.BH_NW]
            if self.SW_bodies:
                self.BH_SW = Quadtree(self.SW, self.SW_bodies)
                subtrees += [self.BH_SW]
            if self.SE_bodies:
                self.BH_SE = Quadtree(self.SE, self.SE_bodies)
                subtrees += [self.BH_SE]

        self.subtrees = subtrees

    def insert(self, body):
        """
        Inserts body into the mass array for the node, and updates the center of
        mass accordingly.  Regenerates the corresponding subregion tree if
        necessary
        """
        global node_list
        self.bodies += [body]
        try:
            self.body = self.body.sum(body)
        except AttributeError:
            print("\nWarning: AttributeError when attempting to insert body.\nThis is only a problem if it happens more than once in an iteration.")
            self.body = body
            self.bodies = [body]

        if len(self.bodies) > 1:
            if body.in_region(self.NE):
                self.NE_bodies += [body]
                self.BH_NE = Quadtree(self.NE, self.NE_bodies)
            elif body.in_region(self.NW):
                self.NW_bodies += [body]
                self.BH_NW = Quadtree(self.NW, self.NW_bodies)
            elif body.in_region(self.SW):
                self.SW_bodies += [body]
                self.BH_SW = Quadtree(self.SW, self.SW_bodies)
            elif body.in_region(self.SE):
                self.SE_bodies += [body]
                self.BH_SE = Quadtree(self.SE, self.SE_bodies)
            else:
                pass

        if len(self.bodies) == 1:
            pass

    def isFar(self, body):
        """
        Calculates metric for determining whether or not to transverse the quadtree
        further when calculating force.
        """
        global theta
        s = self.region.sidelength
        d = self.body.distance_to(body)
        return ( ( s/d ) < theta )

    def get_force(self, body):
        """
        Calculate the force that self exerts on body.  If the calling object
        is a single particle, use simple newton's law.  Else, if it's sufficiently
        far away, treat self like a cluster of particles stored at their center of
        mass. If it's not, then recurse into the subtree structure and repeat.
        """
        if len(self.bodies) == 1 and self.body != body:
            distance_tuple = body.distance_to(self.body)
            numerator = ( -6.67 * ( 10 ** ( -11 ) ) * self.body.mass * body.mass)
            body.frc += np.array([numerator/(distance_tuple[0]**2), numerator/(distance_tuple[1]**2)])

        else:
            if self.isFar(body):
                distance_tuple = body.distance_to(self.body)
                numerator = (-6.67 * ( 10** ( -11 ) ) * self.body.mass * body.mass)
                body.frc += np.array([numerator/(distance_tuple[0]**2), numerator/(distance_tuple[1]**2)])

            else:
                for subtree in self.subtrees:
                    subtree.get_force(body)

class System:
    """
    Overall wrapper
    """
    def __init__(self, max_t, dt, corners, m_list = [], threshold = .1, name="test"):
        """
        masses should be passed as np arrays of [mass, [x,y], [vx,vy] ]
        """
        os.mkdir(name)
        os.chdir(name)

        self.max_t = max_t
        self.dt = dt

        self.m_list = m_list
        self.threshold = threshold
        self.space = BoundRegion(corners)
        self.NW = corners[1]

    def start(self):
        bar = progressbar.ProgressBar()
        for time in bar(range(0, self.max_t, self.dt)):
            print("\ntimestep:", time, "of", self.max_t/self.dt)
            self.update('{:0>8}'.format( str( time ) ) + ".png" )


    def to_pixel(self, pos, width, sidelength):
        """
        pos should be numpy array, width should be pixel length of picture, e.g. 2000,
        sidelength should be sidelength of the space.
        """
        if self.space.contains(pos):
            rel_pos = pos - self.NW #self.NW is (0,0) in PIL
            rel_pos[1] = -1*rel_pos[1] # flip the sign
            rel_pos = rel_pos/sidelength
            rel_pos *= width
            rel_pos = np.rint(rel_pos).astype(int)
            return rel_pos

    def update(self, filename):
        """

        """
        self.masterTree = Quadtree(self.space)

        canvas = Image.new("RGB", (2000,2000))
        draw = ImageDraw.Draw(canvas)
        bar = progressbar.ProgressBar()

        for mass in bar(self.m_list):
            body = Body(m_array = np.array(mass[0]), pos_array = np.array(mass[1]), v_array = np.array(mass[2]))
            self.masterTree.insert(body)
            try:
                draw.point( self.to_pixel( body.pos, 2000, self.space.sidelength ), fill = (245, 245, 245) )
            except TypeError:
                pass
        canvas.save(filename, format="PNG")
        print("\ncalculating forces...")
        for body in self.masterTree.bodies:
            for node in self.masterTree.subtrees:
                node.get_force(body)
        for body in self.masterTree.bodies:
            body.update(self.dt)

def parse(filename):
    """
    takes as input a data file with each row of following format:
    x_pos y_pos x_vel y_vel mass
    yes.  It's delimited by whitespace.  aaaaaaaaaa

    not super necessary probably but it works?
    """
    file = open(filename, 'r')
    data = file.read()
    to_format = data.split( "\n" )
    to_write = ""
    for row in to_format:
        crap = row.split(" ")
        crap = crap[:5]
        to_write += " ".join(crap) + "\n"
    file = open(filename, 'w')
    file.write(to_write)

def ingest(filename):
    """
    takes as input a .txt data file for galaxy data and outputs an array
    of the format required for System.__init__
    """
    file = open(filename, 'r')
    data = file.read()
    star_list = data.split( "\n" )
    radius = star_list[1]
    m_list = []
    for star in star_list:
        if star:
            star = star.split(" ")
            for i in range(5):
                star[i] = float(star[i])
            m_list += [ [ np.array( [ star[4] ] ), np.array( [ [ star[0], star[1] ] ]), np.array( [ [ star[2], star[3] ] ] ) ] ]
    #print(m_list)
    return (radius, m_list)

def test():
    home_dir = os.getcwd()
    #try:
    m_list = ingest("data.txt")
    corners = [ np.array([2.83800E06, 2.83800E06]), np.array([-2.83800E06, 2.83800E06]), np.array([-2.83800E06, -2.83800E06]), np.array([2.83800E06, -2.83800E06]) ]
    test = System(100000, 1000, corners, m_list)
    test.start()
    #except:
        #os.chdir(home_dir)
        #subprocess.run(["rm", "-rf", "test/"])

def wrapper(filename):
    """
    Takes as input a string corresponding to the name of a file in ./rawdata/
    and sets the parameters for the system.
    """
    home_dir = os.getcwd()
    #os.mkdir("processed_data")
    #os.chdir("processed_data")
    #processed_dir = os.getcwd()
    #os.chdir("..")
    os.chdir("raw_data")
    file = open(filename, "r")
    data = file.read()
    data_list = data.split( "\n" )
    radius = float(data_list[1])
    m_list = []
    for star in data_list[2:]:
        if star:
            star = star.split(" ")
            for i in range(5):
                star[i] = float(star[i])
            for i in range(5,8):
                star[i] = int(star[i])
            m_list += [ [ np.array( [ star[4] ] ), np.array( [ [ star[0], star[1] ] ] ), np.array( [ [ star[2], star[3] ] ] ), ( star[5], star[6], star[7] ) ] ]
    os.chdir("..")
    test_dir = home_dir + "/tests/"
    if ~os.path.exists(test_dir):
        os.mkdir("tests")
    else:
        delete = input("dir \"tests\" already exists.  Remove it? Enter yes to confirm, and any other char will cancel it.")
    os.chdir("tests")
    file_dir = os.getcwd() +  str(filename)
    cd(file_dir)

    os.chdir(home_dir)
