# Create a sphere object. with a radius of .5.
# This sphere should be fixed and not move

my_sphere = sphere(center=(0,0,0),radius=.5,fixed=True)

# Add a second sphere, 4 _ above the first one whiche is free, subject to dyamics

my_sphere_free = sphere(center=(0,0,4),radius=.5,fixed=False)

# Add the spheres to the simulation

O.bodies.append([my_sphere, my_sphere_free])

# Set up the simulation loop to add physical properties

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

# now we can set the timestep for our simulation. There is a critical value
# given with PWaveTimeStep(). The timestep should not be larger than this value
# you can experiment with the timestep and see what happens
O.dt=.5e-4*PWaveTimeStep() #TODO what is the PWaveTimeStep?

# save the simulation, so that it can be reloaded later, for experimentation
O.saveTmp() #TODO what exactly dose this do?
