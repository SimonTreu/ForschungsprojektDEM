################################
##  Define Simulation Bodies  ##
################################


# create fixed sphere and two spheres above 'sticking together'
spheres = []
# create cohesive Material

idLimestone = O.materials.append(CohFrictMat(
young=30e3,poisson=.2,density=2700,frictionAngle=radians(0),
isCohesive=True,normalCohesion=25e6,shearCohesion=50e6,
etaRoll=0.1,momentRotationLaw=True,alphaKr=0.1,alphaKtw=0.1,label="sphereMat"))
idNonCohesiveLimesone = O.materials.append(
   CohFrictMat(young=30e3,poisson=.2,density=2700,frictionAngle=radians(0),
isCohesive=True)
)

spheres.append(sphere(center=(0,0,0), radius=1, fixed=True, material=idNonCohesiveLimesone))



spheres.append(sphere(center=(0, -1, 3), radius=1, fixed=True, material=idLimestone))
spheres.append(sphere(center=(0, 1, 3), radius=1, fixed=False, material=idLimestone))

O.bodies.append(spheres)

O.engines=[
   ForceResetter(),
   InsertionSortCollider([Bo1_Sphere_Aabb()]),
   InteractionLoop(
   [Ig2_Sphere_Sphere_ScGeom()],
   [Ip2_FrictMat_FrictMat_FrictPhys(),
   Ip2_CohFrictMat_CohFrictMat_CohFrictPhys(setCohesionNow=False,label="cohesiveIp")],
   [Law2_ScGeom_FrictPhys_CundallStrack(),
   Law2_ScGeom6D_CohFrictPhys_CohesionMoment(useIncrementalForm=True,label='cohesiveLaw')]
   ),
   NewtonIntegrator(damping=0.8,gravity=[0,0,-9.81]),
]
O.dt=.5e-5*PWaveTimeStep()
O.save()
