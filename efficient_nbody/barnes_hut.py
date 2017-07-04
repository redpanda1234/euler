import numpy as np
import time
import math

# for drawing out resulting frames
from Pillow import Image, ImageDraw

# get numpy to actually throw errors, instead of just printing them.
np.seterr(all='raise')

# threshold s/d value for determining whether to recurse into tree
theta = 0.5

class BoundRegion:
    """
    BoundRegion class represents a square on the grid we're simulating over.

    """
    def __init__(self, corners):
        """
        Takes as input an array of 4 numpy arrays containing the (x,y) pairs
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
        self.get_sidelength()

    def get_sidelength(self):
        """
        This method uses the points on the square to get its sidelength.
        Maybe just do this hard-coded instead of with a method?
        """
        self.sidelength = (self.NE_corner[0] - self.NW_corner[0])
        return self.sidelength

    def contains(self, point):
        """
        This method takes as input an array defining a point, and checks if the
        point is within the borders of the region.  Returns bool.
        """
        x,y = point # get the x and y coodinates out of the point array
        # similarly, use the splat operator * to unpack the x,y for corners
        lower_x, lower_y, upper_x, upper_y = [*self.SW_corner, *self.NE_corner]
        if lower_x < x and x < upper_x: # check if x in bounds
            if lower_y < y and y < upper_y: # and check if y in bounds
                return True
        return False

    def get_NE(self):
        """
        This method returns a sub-region of the calling region, corresponding
        to the north-east quadrant (quadrant I)
        """
        NE = self.NE_corner
        NW = self.N
        SW = self.center
        SE = self.E
        print(NE,NW,SW,SE)
        return BoundRegion(((NE, NW, SW, SE)))

    def get_NW(self):
        """
        This method returns a sub-region of the calling region, corresponding
        to the north-west quadrant (quadrant II)
        """
        NE = self.N
        NW = self.NW_corner
        SW = self.W
        SE = self.center
        print(NE,NW,SW,SE)
        return BoundRegion(((NE, NW, SW, SE)))

    def get_SW(self):
        """
        This method returns a sub-region of the calling region, corresponding
        to the south-west quadrant (quadrant III)
        """
        NE = self.center
        NW = self.W
        SW = self.SW_corner
        SE = self.S
        print(NE,NW,SW,SE)
        return BoundRegion(((NE, NW, SW, SE)))

    def get_SE(self):
        """
        This method returns a sub-region of the calling region, corresponding
        to the south-east quadrant (quadrant IV)
        """
        NE = self.E
        NW = self.center
        SW = self.S
        SE = self.SE_corner
        print(NE,NW,SW,SE)
        return BoundRegion(((NE,NW,SW,SE)))

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

        self.vel = v_array
        self.frc = f_array
        self.sub_bodies = sub_bodies

        self.mass = self.get_mass()
        if self.mass != 0:
            self.pos = self.get_CoM() # define position as center of mass
        else:
            self.pos = None

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
        return (np.dot(transposed_mass_array, self.pos_array))/self.mass


    def update(self, dt):
        """
        This method uses Euler's method to update position and velocity
        of the body over a small time interval dt
        """
        self.vel += dt * self.frc / self.mass
        self.pos += dt * self.vel

    def distance_to(self, other_body):
        """
        This method returns a tuple of the displacement in x and y between
        the calling body (self) and the second body (other_body)
        """
        return (self.pos[0]-other_body.pos[0], self.pos[1]-other_body.pos[1])
        #return np.linalg.norm(self.pos - other_body.pos)

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
        pos_array = np.append(self.pos_array, other_body.pos_array)
        return Body(m_array, pos_array)

    def reset(self):
        """
        resets the force array to 0 so that forces don't pile up over
        timesteps.
        """
        self.frc = np.array([0,0])

    def draw(self, canvas):
        """

        """
        pass


class Quadtree:

    def __init__(self, region, bodies = []):
        """
        Quadtree creates an object to store the Barnes-hut tree for the n-body
        simulator.  Each node corresponds to an object of type Quadtree and its
        corresponding region and body.  Recursive generation stops when a region
        contains either 0 or 1 bodies.
        """
        self.region = region # store reference to region in node
        self.bodies = bodies #

        if len(bodies) > 1: # subdivide if more than 1 body in region

            self.NE = region.get_NE
            self.NW = region.get_NW
            self.SW = region.get_SW
            self.SE = region.get_SE

            self.NE_bodies = [body for body in bodies if body.in_region(self.NE)]
            self.NW_bodies = [body for body in bodies if body.in_region(self.NW)]
            self.SW_bodies = [body for body in bodies if body.in_region(self.SW)]
            self.SE_bodies = [body for body in bodies if body.in_region(self.SE)]

            self.BH_NE = Quadtree(self.NE, self.NE_bodies)
            self.BH_NW = Quadtree(self.NW, self.NW_bodies)
            self.BH_SW = Quadtree(self.SW, self.SW_bodies)
            self.BH_SE = Quadtree(self.SE, self.SE_bodies)

    def insert(self, body):
        """
        Inserts body into the mass array for the node, and updates the center of
        mass accordingly.  Regenerates the corresponding subregion tree if
        necessary
        """
        self.bodies += body

        try:
            self.body = self.body.sum(body)
        except:
            self.body = body

        if body.in_region(self.NE):
            self.NE_bodies += body
            self.BH_NE = Quadtree(self.NE, self.NE_bodies)
        elif body.in_region(self.NW):
            self.NW_bodies += body
            self.BH_NW = Quadtree(self.NW, self.NW_bodies)
        elif body.in_region(self.SW):
            self.SW_bodies += body
            self.BH_SW = Quadtree(self.SW, self.SW_bodies)
        elif body.in_region(self.SE):
            self.SE_bodies += body
            self.BH_SE = Quadtree(self.SE, self.SE_bodies)
        else:
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
                for subtree in [self.BH_NE, self.BH_NW, self.BH_SW, self.BH_SE]:
                    subtree.get_force(body)



class System:
    """
    Overall wrapper
    """

    def __init__(self, max_t, dt, corners, m_list = [], threshold = .1):
        """
        masses should be passed as np arrays of [mass, [x,y], [vx,vy] ]
        """
        self.masses = m_list
        self.threshold = threshold
        self.space = BoundRegion(corners)
        self.NW = corners[1]

    def start(self):
        for time in range(0, max_t, dt):
            self.update('{:0>8}'.format( str( time ) ) )


    def to_pixel(self, pos, width, sidelength):
        """
        width and height should be pixel values for the output image, e.g.
        1920 x 1080.
        """
        if self.space.contains(pos):
            rel_pos = pos - self.NW
            rel_pos[1] -= 2*rel_pos[1] # flip the sign
            rel_pos = rel_pos/sidelength
            rel_pos *= width
            return rel_pos

    def update(self, filename):
        """

        """
        self.masterTree = Quadtree(self.region)

        for mass in m_list:
            body = Body(np.array(mass[0]), np.array(mass[1]), np.array(mass[2]))
            self.masterTree.insert(body)
            canvas = Image.open(str(filename))
            draw = Image.Draw(canvas)

            try:
                draw.point( self.to_pixel( body.pos, 1920, self.space.sidelength ) )
            except TypeError:
                pass

#def test(10000, 100, np.array( [1000, np.array( [ ] ) ] )):
