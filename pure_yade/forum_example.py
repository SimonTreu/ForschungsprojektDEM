#exercicio de Law

# basic simulation showing sphere falling ball gravity,
# bouncing against another sphere representing the support

# DATA COMPONENTS

# add 2 particles to the simulation
# they the default material (utils.defaultMat)

matSph=CohFrictMat(
 young=170e6,
 poisson=0.2,
 frictionAngle=radians(17),
 isCohesive=False,
 alphaKr=1.8,
 alphaKtw=0,
 etaRoll=1.8,
 momentRotationLaw=True,
 density=2600,
 label='spheres',
)

O.materials.append(matSph)

O.bodies.append([
# fixed: particle's position in space will not change (support)
utils.sphere(center=(0,0,0),radius=.5,fixed=True,material='spheres'),
# this particles is free, subject to dynamics
utils.sphere((0,0,2),.5,material='spheres')
])

# FUNCTIONAL COMPONENTS

# simulation loop -- see presentation for the explanation
O.engines=[
ForceResetter(),
InsertionSortCollider([Bo1_Sphere_Aabb()]),
InteractionLoop(
[Ig2_Sphere_Sphere_ScGeom6D()],
[Ip2_CohFrictMat_CohFrictMat_CohFrictPhys(label="cohesiveIp")],
[Law2_ScGeom6D_CohFrictPhys_CohesionMoment(label="cohesiveLaw")]

),
# apply gravity force to particles
GravityEngine(gravity=(0,0,-9.81)),
# damping: numerical dissipation of energy
NewtonIntegrator(damping=0.1)
]

O.dt=.5e-3*utils.PWaveTimeStep()
