import numpy as np

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

class Quadrant:

    def __init__(self, m_list, corners):
        self.m_list = m_list
        self.region = BoundRegion(corners)
        self.center = self.region.center
        self.mass = self.get_mass()
        self.CoM = self.get_CoM()

    def get_mass():
        pass

    def get_CoM():
        for mass in m_list:

    def in_region(self, region):
        return self.center

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
