from yadeimport import *
import numpy as np

a = sphere(center=(0,0,0),radius=0.5)
foo = a.shape
foo2 = a.state
print np.array(foo2.pos)