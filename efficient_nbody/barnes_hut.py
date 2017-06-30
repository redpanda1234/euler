import numpy as np
import time
import math

class BoundRegion:

    def __init__(self, corners):
        """ corners should be a list of 4 (x,y) numpy arrays
        """
        self.NE_corner, self.NW_corner, self.SW_corner, self.SE_corner = corners

        self.N = .5 * (self.NE_corner + self.NW_corner)
        self.W = .5 * (self.NW_corner + self.SW_corner)
        self.S = .5 * (self.SW_corner + self.SE_corner)
        self.E = .5 * (self.SE_corner + self.NE_corner)

        self.center = .25 * (self.N + self.W + self.S + self.E)

        self.get_sidelength()

    def get_sidelength(self):
        """
        """
        self.sidelength = (self.NE_corner[0] - self.NW_corner[0])
        return self.sidelength

    def contains(self, point):
        """
        """
        x,y = point
        lower_x, lower_y, upper_x, upper_y = [*self.SW_corner, *self.NE_corner]
        if lower_x < x and x < upper_x:
            if lower_y < y and y < upper_y:
                return True
        return False

    def get_NE(self):
        """
        """
        NE = self.NE_corner
        NW = self.N
        SW = self.center
        SE = self.E
        print(NE,NW,SW,SE)
        return BoundRegion(((NE, NW, SW, SE)))

    def get_NW(self):
        """
        """
        NE = self.N
        NW = self.NW_corner
        SW = self.W
        SE = self.center
        print(NE,NW,SW,SE)
        return BoundRegion(((NE, NW, SW, SE)))

    def get_SW(self):
        """
        """
        NE = self.center
        NW = self.W
        SW = self.SW_corner
        SE = self.S
        print(NE,NW,SW,SE)
        return BoundRegion(((NE, NW, SW, SE)))

    def get_SE(self):
        NE = self.E
        NW = self.center
        SW = self.S
        SE = self.SE_corner
        print(NE,NW,SW,SE)
        return BoundRegion(((NE,NW,SW,SE)))

class Body:

    def __init__(self, m_array, pos_array, p_array, v_array, f_array, sub_bodies = []):
        self.m_array = m_array
        self.pos_array = pos_array

        self.pos = p_array
        self.vel = v_array
        self.frc = f_array
        self.sub_bodies = sub_bodies
        self.mass = self.get_mass()
        self.CoM = self.get_CoM()

    def get_mass(self):
        total_mass = 0
        for mass in self.m_array:
            total_mass += mass
        return total_mass

    def get_CoM(self):
        """
        ok this is really cool: center of mass equation is essentially the
        inner product of a mass vector and a matrix of position vectors!
        """
        transposed_mass_array = self.m_array.T
        return (np.dot(transposed_mass_array, self.pos_array))/self.mass

    def update(self, dt):
        """
        """
        self.vel += dt * self.frc / self.mass
        self.pos += dt * self.vel

    def distance_to(self, other_body):
        return np.linalg.norm(self.pos - other_body.pos)

    def in_region(self, region):
        """
        """
        return region.contains(self.CoM)


    def sum(self, other_body):
        """
        """
        m_array = np.append(self.m_array, other_body.m_array)
        pos_array = np.append(self.pos_array, other_body.pos_array)
        return Body(m_array, pos_array)


class Node:

    def __init__(self, **kwargs):
       pass

class Octree:

    def __init__(self, m_list = []):
        self.m_list = m_list
        self.root = self.m_list[0]
        self.constructor(self.root)
        self.children = []

    def constructor(root):
        pass

class n_body_system:
    """
    """
    def __init__(self, m_list = [], threshold = .1):
        """
        """
        self.masses = m_list
        self.threshold = threshold

    def get_center_of_mass(m_list):
        """ masses should contain
        """
        for mass in m_list:
            pass

def test():
    corners = np.array([np.array([1,1]), np.array([-1,1]), np.array([-1,-1]), np.array([1,-1])])

    test_region = BoundRegion(corners)
    assert test_region.contains(np.array([0,0]))
    assert ~test_region.contains(np.array([-1,1]))
    test_region.get_NE()
    test_region.get_NW()
    test_region.get_SW()
    test_region.get_SE()

    m_array = np.array([1,1,1,1])
    pos_array = np.array([
        [1,1,0],
        [-1,1,0],
        [-1,-1,0],
        [1,-1,0]
    ])
    corners = np.array([[4,4],[-4,4],[-4,-4],[4,-4]])
    test_quad = Quadrant(m_array, pos_array, corners)
    print(test_quad.CoM, test_quad.center)
    #print(test_quad.in_region(BoundRegion()))
