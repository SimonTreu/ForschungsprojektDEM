from yade import utils,ymport,export
packing='alignedBox_4'

def sphereMat():
    return JCFpmMat(type=1,young=1,frictionAngle=radians(1),
                    density=1,poisson=1,tensileStrength=1e6,cohesion=1e6,
                    jointNormalStiffness=1,jointShearStiffness=1,jointTensileStrength=1e6,
                    jointCohesion=1e6,jointFrictionAngle=1)

O.bodies.append(ymport.text('data/'+packing+'.spheres',scale=1,shift=Vector3(0,0,0),material=sphereMat)) #(-3,-4,-8)

dim=utils.aabbExtrema()
xinf=dim[0][0]
xsup=dim[1][0]
yinf=dim[0][1]
ysup=dim[1][1]
zinf=dim[0][2]
zsup=dim[1][2]

print 'YINF  =  ',yinf

for o in O.bodies:
    if isinstance(o.shape,Sphere):
        o.shape.color=(.3,.5,.5)
    if o.state.pos[1] < (yinf + .5):
        o.state.blockedDOFs += 'xyz'
        o.shape.color = (1, 1, 1)

############################ engines definition
interactionRadius=1.;
O.engines=[

	ForceResetter(),
	InsertionSortCollider([Bo1_Sphere_Aabb(aabbEnlargeFactor=interactionRadius,label='is2aabb'),Bo1_Facet_Aabb()]),
	InteractionLoop(
		[Ig2_Sphere_Sphere_ScGeom(interactionDetectionFactor=interactionRadius,label='ss2d3dg'),Ig2_Facet_Sphere_ScGeom()],
		[Ip2_JCFpmMat_JCFpmMat_JCFpmPhys(cohesiveTresholdIteration=1,label='interactionPhys')],
		[Law2_ScGeom_JCFpmPhys_JointedCohesiveFrictionalPM(smoothJoint=True,label='interactionLaw')]
	),
	NewtonIntegrator(damping=1)

]

############################ timestep + opening yade windows
O.dt=0.001*utils.PWaveTimeStep()

from yade import qt
v=qt.Controller()
v=qt.View()

O.step()

export.text('data/'+packing+'_processed'+'.spheres')
export.textExt('data/'+packing+'_processed_jointedPM.spheres',format='jointedPM')

O.wait()

############################