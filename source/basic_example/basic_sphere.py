# Create a material object of type FrictMat with the elastic properties of steal
steel = FrictMat(young=210e9,poisson=.25,frictionAngle=.8,label="steel")
# Add the material to the simulation and save the id to assign it to materials
idSteel=O.materials.append(steel)
# Create a sphere object. with a radius of .5.
# This sphere should be fixed and not move
my_sphere = sphere(center=(0, 0, 0), radius=.5, fixed=True, material=idSteel)

# Add a second sphere, 4 _ above the first one whiche is free, subject to dyamics

my_sphere_free = sphere(center=(0, 0, 4), radius=.5, fixed=False, material=idSteel)

# Add the spheres to the simulation

O.bodies.append([my_sphere, my_sphere_free])

# Set up the simulation loop to add physical properties

O.engines=[
    ForceResetter(),
    # Add a "Collider" that approximates if two Objects are interacting
    # InsertionSortCollider dose that using an insertion sort algorithm
    InsertionSortCollider([Bo1_Sphere_Aabb()]),
    # The Interaction loop is run for all Particles that are approximatet to interact
    # by the Collider
    InteractionLoop(
        [Ig2_Sphere_Sphere_ScGeom()], # This class Calculates
        # when exactly two spheres collide. We could also add multiple classes here if
        # we had different objects in the simulation
        [Ip2_FrictMat_FrictMat_FrictPhys()], # Adds a collition Physics
        [Law2_ScGeom_FrictPhys_CundallStrack()]
    ),
    # Applies all calculated forces and gravity to the particles
    # It also intruduces a damping factor which acts as a numerical dissipation of
    # energy
    NewtonIntegrator(gravity=(0, 0, -9.81), damping=0.1)
]

# now we can set the timestep for our simulation. There is a critical value
# given with PWaveTimeStep(). The timestep should not be larger than this value
# you can experiment with the timestep and see what happens
O.dt=1e-4*PWaveTimeStep()
