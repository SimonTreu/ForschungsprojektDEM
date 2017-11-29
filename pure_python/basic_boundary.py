from my_sphere_creators import *
import numpy as np

x_range = [-1.5, 1.5]
y_range = [-1.5, 1.5]
z = 0
radius = .5
distance = 2 * radius + .5
creator = FixedBoundarySpheresCreator(x_range, y_range, z)
centers = creator.create_centers(distance)
spheres = creator.create_spheres(centers, radius)
my_sphere_free = sphere(center=(0,0,4),radius=.5,fixed=False)
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

O.dt=.5*PWaveTimeStep() #TODO what is the PWaveTimeStep?

# save the simulation, so that it can be reloaded later, for experimentation
O.saveTmp() #TODO what exactly dose this do?