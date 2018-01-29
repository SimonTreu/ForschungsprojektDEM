################################
##  Define Simulation Bodies  ##
################################

horizontal = True
# create fixed sphere and two spheres above 'sticking together'
spheres = []
# create cohesive Material

idLimestone = O.materials.append(
   CohFrictMat(young=170e6,
               poisson=0.2,
               density=2700,
               frictionAngle=radians(0),
               isCohesive=True,
               normalCohesion=25e6,
               shearCohesion=50e6,
               etaRoll=0.1,
               momentRotationLaw=True,
               alphaKr=0.1,
               alphaKtw=0.1,
               label="sphereMat")
)

spheres.append(sphere(center=(0,1,0), radius=1, fixed=True, material='sphereMat'))
if horizontal:
    pass
else:
    h= [10,14]

    spheres.append(sphere(center=(0, 1, h[1]), radius=1, fixed=True, material='sphereMat'))
    for i in range(h[0],h[1],2):
        spheres.append(sphere(center=(0, 1, i), radius=1, fixed=False, material='sphereMat'))

O.bodies.append(spheres)

O.engines=[
   ForceResetter(),
   InsertionSortCollider([Bo1_Sphere_Aabb(aabbEnlargeFactor=1.6)]),
   InteractionLoop(
   [Ig2_Sphere_Sphere_ScGeom6D(interactionDetectionFactor=1.6)],
   [
   Ip2_CohFrictMat_CohFrictMat_CohFrictPhys(setCohesionNow=True, label="cohesiveIp")],
   [
   Law2_ScGeom6D_CohFrictPhys_CohesionMoment(label='cohesiveLaw')]
   ),
   NewtonIntegrator(damping=0.8,gravity=[0,0,-9.81]),
]
O.dt=.5e-3*PWaveTimeStep()
