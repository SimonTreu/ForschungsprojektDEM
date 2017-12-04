import numpy as np

# The imported files below could not be imported with the standard python error as this lead to an error
# in yade, which could not find the files. Untill this is fixed I made hard copys of the code. Please
# do not change this code here, but rather in the original files and copy it here afterwards.


#############################################
###  imported from my_sphere_creators.py  ###
#############################################

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
            my_spheres.append(sphere(center=c, radius=radius, fixed=fixed, color=(1,0,0)))
        return  my_spheres

########################################
### Imported from sphere_selector.py ###
########################################

def select_spheres_in_circle_on_plane(spheres, center, radius):

    center = np.array(center)

    spheres_inside_bsphere = []
    spheres_outside_bsphere = []

    while len(spheres) > 0:
        s = spheres.pop()
        c = np.array(s.state.pos)
        c -= center
        if np.linalg.norm(c) <= radius:
            spheres_inside_bsphere.append(s)
        else:
            spheres_outside_bsphere.append(s)

    return spheres_inside_bsphere, spheres_outside_bsphere

########################################################################################################

###################
###  Yade Code  ###
###################

#---------------------------#
#--  boundary conditions  --#
#---------------------------#

# Set the variables for the bottom plane of spheres:
x_range = [-9, 9]
y_range = [-9, 9]
z_range = [-9, 9]
z = z_range[0]

radius = .5
distance = 2 * radius

creator = FixedBoundarySpheresCreator(x_range, y_range, z)
centers = creator.create_centers(distance)
spheres = creator.create_spheres(centers, radius, fixed=True)

# Select spheres within a boundary sphere around the (0,0,-9)

spheres_inside_bsphere, spheres_outside_bsphere = select_spheres_in_circle_on_plane(spheres=spheres,
                                                                                    center=(0,0,-9), radius=3)
#Add disappearing spheres to simulation and safe their indices
indexes_of_disappearing_spheres = O.bodies.append(spheres_inside_bsphere)

#Add stable spheres to simulation (we don't need the indices now)
O.bodies.append(spheres_outside_bsphere)

#Add boundary box to simulation
O.bodies.append(geom.facetBox(center=(0, 0, 0), extents=(9, 9, 9), wallMask=15))

#----------------------#
#--  filling the box --#
#----------------------#

#Specify material
#idSteel=O.materials.append(FrictMat(young=210e9,poisson=.25,frictionAngle=.8,label="steel"))

#Generate loose spheres as granular material
#sp = pack.SpherePack()
# sp = pack.
# # generate randomly spheres with uniform radius distribution
# sp.makeCloud((-8, -8, -8), (8, 8, 8), rMean=.4, rRelFuzz=.5, porosity=0.05)
# # add the sphere pack to the simulation
# sp.toSimulation(color=(.5, .3, 0))

#####
idConcrete=O.materials.append(FrictMat(young=30e9,poisson=.2,frictionAngle=.6,label="concrete"))
pred=pack.inAlignedBox(minAABB=(-9,-9,-8), maxAABB=(9,9,0))
spheres=pack.randomDensePack(pred, radius=.5, rRelFuzz=.8,  returnSpherePack=True, spheresInCell=300, material=idConcrete)
spheres.toSimulation(color=(.5, .3, 0))
#-----------------------#
#--  Add the engines  --#
#-----------------------#

O.engines = [
    ForceResetter(),  # TODO not shure why we need this
    # Add a "Collider" that approximates if two Objects are interacting
    # InsertionSortCollider dose that using an insertion sort algorithm
    InsertionSortCollider([Bo1_Sphere_Aabb(), Bo1_Facet_Aabb()]),
    # The Interaction loop is run for all Particles that are approximatet to interact
    # by the Collider
    InteractionLoop(
        [Ig2_Sphere_Sphere_ScGeom(), Ig2_Facet_Sphere_ScGeom()],  # This class Calculates
        # when exactly two spheres collide. We could also add different Classes here if
        # we had different objects in the simulation
        [Ip2_FrictMat_FrictMat_FrictPhys()],  # Adds a collition Physics TODO look up what exactly
        [Law2_ScGeom_FrictPhys_CundallStrack()]  # TODO what happens here? condact law -- apply forces
    ),
    # Applies all calculated forces and gravity to the particles and calculates
    # a new position TODO also velocity and acceleration?
    # It also intruduces a damping factor which acts as a numerical dissipation of
    # energy
    NewtonIntegrator(gravity=(0, 0, -9.81), damping=0.1),
    PyRunner(command='removeNextSphere()', realPeriod=1)
]

# specify timestep
O.dt = PWaveTimeStep()

#----------------------------------------------#
#--  remove spheres from running simulation  --#
#----------------------------------------------#

def removeNextSphere():
    n = len(indexes_of_disappearing_spheres)
    if n > 0:
        r = np.random.randint(n)
        id = indexes_of_disappearing_spheres.pop(r)
        O.bodies.erase(id)
