import numpy as np

class FixedBoundarySpheresCreator:
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

    def create_spheres(self, centers, radius, fixed=False):
        my_spheres = []
        for c in centers:
            my_spheres.append(sphere(center=c, radius=radius, fixed=fixed))
        return  my_spheres

# Add the boundary conditions

x_range = [-3, 3]
y_range = [-3, 3]
z = 0
radius = .5
distance = 2 * radius + .8
creator = FixedBoundarySpheresCreator(x_range, y_range, z)
centers = creator.create_centers(distance)
spheres = creator.create_spheres(centers, radius, fixed=True)

# Add my own free falling spheres


for center in [(0,.1,4),(0,-.1,6)]:
    my_sphere_free = sphere(center=center,radius=.5,fixed=False)
    spheres.append(my_sphere_free)

O.bodies.append(spheres)

O.engines=[
    ForceResetter(), #TODO not shure why we need this
    # Add a "Collider" that approximates if two Objects are interacting
    # InsertionSortCollider dose that using an insertion sort algorithm
    InsertionSortCollider([Bo1_Sphere_Aabb()]),
    # The Interaction loop is run for all Particles that are approximatet to interact
    # by the Collider
    InteractionLoop(
        [Ig2_Sphere_Sphere_ScGeom()], # This class Calculates
        # when exactly two spheres collide. We could also add different Classes here if
        # we had different objects in the simulation
        [Ip2_FrictMat_FrictMat_FrictPhys()], # Adds a collition Physics TODO look up what exactly
        [Law2_ScGeom_FrictPhys_CundallStrack()] #TODO what happens here? condact law -- apply forces
    ),
    # Applies all calculated forces and gravity to the particles and calculates
    # a new position TODO also velocity and acceleration?
    # It also intruduces a damping factor which acts as a numerical dissipation of
    # energy
    NewtonIntegrator(gravity=(0, 0, -9.81), damping=0.1)
]

O.dt=.6e-4*PWaveTimeStep() #TODO what is the PWaveTimeStep?

# save the simulation, so that it can be reloaded later, for experimentation
O.saveTmp() #TODO what exactly dose this do?