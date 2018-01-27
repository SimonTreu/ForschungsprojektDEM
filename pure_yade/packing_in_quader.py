from yade import pack,export

sizeRatio=4. # defines discretisation (sizeRatio=meshLength/particleDiameter)

mesh='alignedBox' #name of gts mesh
pred=pack.inAlignedBox((-2,-2,-.5),(2,2,.5))
# get characteristic dimensions
aabb = pred.aabb()
dim = pred.dim()
center = pred.center()
minDim = min(dim[0], dim[1], dim[2])
# define discretisation
radius = minDim / (2 * sizeRatio)

print radius

sp = pack.randomDensePack(pred, radius=radius, rRelFuzz=0.3, useOBB=True, memoizeDb='/tmp/gts-triax-packings.sqlite',
                          returnSpherePack=True)  # cropLayers=5 (not to use)
sp.toSimulation(color=(0.9, 0.8, 0.6))

export.text('data/'+mesh+'_'+str(int(sizeRatio))+'.spheres')

#### VIEW
from yade import qt
qt.View()