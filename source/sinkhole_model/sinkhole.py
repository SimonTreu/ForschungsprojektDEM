from yade import plot, pack, utils, ymport
import numpy as np

def is_inside_sphere(center, r, point):
    c = np.array(point)
    c -= center
    return np.linalg.norm(c) <= r


#### controling parameters
packing='../../data/alignedBox_15'
smoothContact = True
jointFrict = radians(20)
jointDil = radians(0)
output = '../../data/alignedBox_15'
maxIter = 5000


#### define materials. One for loose particles and one for solid rock
nonCohesive = O.materials.append(JCFpmMat(type=0, young=1e8, frictionAngle=radians(30), poisson=0.3, density=3000))


def sphereMat(): return JCFpmMat(type=1, young=1e8, frictionAngle=radians(30), density=3000, poisson=0.3,
                                 tensileStrength=3.5e4, cohesion=1e5)
## Rq: density needs to be adapted as porosity of real rock is different to granular assembly due to difference in porosity (utils.sumForces(baseBodies,(0,1,0))/(Z*X) should be equal to Gamma*g*h with h=Y, g=9.82 and Gamma=2700 kg/m3

#### Import of the sphere assembly and assign the cohesive material property
O.bodies.append(ymport.text(packing + '.spheres', scale=1., shift=Vector3(0, 0, 0), material=sphereMat))

## preprocessing to get dimensions of the packing
dim = utils.aabbExtrema()
dim = utils.aabbExtrema()
xinf = dim[0][0]
xsup = dim[1][0]
X = xsup - xinf
yinf = dim[0][1]
ysup = dim[1][1]
Y = ysup - yinf
zinf = dim[0][2]
zsup = dim[1][2]
Z = zsup - zinf

## preprocessing to get spheres dimensions
R = 0
Rmax = 0
numSpheres = 0.
for o in O.bodies:
    if isinstance(o.shape, Sphere):
        numSpheres += 1
        R += o.shape.radius
        if o.shape.radius > Rmax:
            Rmax = o.shape.radius
Rmean = R / numSpheres

#### Boundary conditions
e = 1.5 * Rmean
Xmax = 0
Ymax = 0
baseBodies = []
removableSpheres=[]

for o in O.bodies:
    if isinstance(o.shape, Sphere):
        o.shape.color = (0.9, 0.8, 0.6)
        ## to fix boundary particles
        if o.state.pos[1] < (yinf + 2 * e):
            o.state.blockedDOFs += 'xyz'
            baseBodies.append(o.id)
            o.shape.color = (1, 1, 1)
        elif o.state.pos[1] > (ysup - 2 * e):
            o.state.blockedDOFs += 'xyz'
            baseBodies.append(o.id)
            o.shape.color = (1, 1, 1)
        elif o.state.pos[0] < (xinf + 2 * e):
            o.state.blockedDOFs += 'xyz'
            baseBodies.append(o.id)
            o.shape.color = (1, 1, 1)
        elif o.state.pos[0] > (xsup - 2 * e):
            o.state.blockedDOFs += 'xyz'
            baseBodies.append(o.id)
            o.shape.color = (1, 1, 1)
            o.shape.wire = True
        #### assign nonCohesive material to all "loose spheres" inside the cuboid.
        elif o.state.pos[2] > (zsup - 6):
            o.mat = O.materials[nonCohesive]
            o.shape.color = (1, 0, .1)

        #### specify spheres that will be removed one by one threw out the simulation
        if is_inside_sphere(center=(0,0,-4),r=2,point=o.state.pos):
            o.shape.color = (.2, .8, .1)
            removableSpheres.append(o.id)


baseBodies = tuple(baseBodies)

#### Engines definition
interactionRadius = 1.  # to set initial contacts to larger neighbours
O.engines = [

    ForceResetter(),
    InsertionSortCollider([Bo1_Sphere_Aabb(aabbEnlargeFactor=interactionRadius, label='is2aabb'), ]),
    InteractionLoop(
        [Ig2_Sphere_Sphere_ScGeom(interactionDetectionFactor=interactionRadius, label='ss2d3dg')],
        [Ip2_JCFpmMat_JCFpmMat_JCFpmPhys(cohesiveTresholdIteration=1, label='interactionPhys')],
        [Law2_ScGeom_JCFpmPhys_JointedCohesiveFrictionalPM(smoothJoint=smoothContact, label='interactionLaw')]
    ),
    GlobalStiffnessTimeStepper(timestepSafetyCoefficient=0.8),
    # VTKRecorder(iterPeriod=500, initRun=True, fileName=(output + '-'), recorders=['spheres', 'velocity', 'intr']),
    PyRunner(command='removeNextSphere()',  virtPeriod=0.1),

    NewtonIntegrator(damping=0.7, gravity=(0., 0., -9.82)),

]

def removeNextSphere():
    n = len(removableSpheres)
    if n > 0:
        r = np.random.randint(n)
        id = removableSpheres.pop(r)
        O.bodies.erase(id)

#### YADE windows
from yade import qt

qt.Controller()
qt.View()

#### time step definition (low here to create cohesive links without big changes in the assembly)
O.dt = 0.5 * utils.PWaveTimeStep()

#### set cohesive links with interaction radius>=1
O.step();
#### initializes now the interaction detection factor to strictly 1
ss2d3dg.interactionDetectionFactor = -1.
is2aabb.aabbEnlargeFactor = -1.

#### RUN!!!
O.dt = 0.1*utils.PWaveTimeStep()
O.run(maxIter)
