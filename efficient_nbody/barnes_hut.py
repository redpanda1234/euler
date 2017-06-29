import numpy as np

class BoundRegion:

    def __init__(self, corners):
        """ corners should be a list of 4 (mass, ())
        """
        self.NE_corner, self.NW_corner, self.SW_corner, self.SE_corner = corners

    def contains(self, point):
        """
        """
        x,y = point
        lower_x, lower_y, upper_x, upper_y = [*self.SW_corner, *self.NE_corner]
        if lower_x < x and x < upper_x:
            if lower_y < y and y < upper_y:
                return True
        return False

    def get_sidelength(self):



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
