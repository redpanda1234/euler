import numpy as np

def get_centroid(point_array):
    """
    point array should be a numpy array of numpy arrays defining
    points
    """
    centroid = np.array([0.,0.])
    for point in point_array:
        centroid += point
    return centroid/len(point_array)

array_1 = np.array([
    np.array([0,1]),
    np.array([1,0]),
    np.array([-1,-1])
])

#array_2 = np.array([
#    np.array([])
#])

#print(get_centroid(array_1))
