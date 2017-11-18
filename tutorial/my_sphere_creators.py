import numpy as np
class FixedBoundarySpheresCreator():
    """
    Function to create spheres with the same radius on a plane

    Parameters
    ----------
    x_range : [float]
        [n , m] min x extend, max x extend
    y_range : [float]
        [n , m] min y extend, max y extend
    z : float
    radius : float
    distance : float

    Returns
    -------
    [sphere]
    """
    def __init__(self, x_range, y_range, z):
        self.x_range = x_range
        self.y_range = y_range
        self.z = z



    def create_centers(self, distance):
        x, y = np.mgrid[
               self.x_range[0]:self.x_range[1] + distance:distance,
               self.y_range[0]:self.y_range[1] + distance:distance
               ]

        x = x.reshape(x.shape[0] * x.shape[1])
        y = y.reshape(y.shape[0] * y.shape[1])

        return [(x[i],y[i],self.z) for i in range(len(x))]

    def create_spheres(self, centers, radius):
        pass