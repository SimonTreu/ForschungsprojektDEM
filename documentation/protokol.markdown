# Protocol of the research project

## Project Structure

### `/source`
This folder contains all Yade scripts. In `/basic_examples` are 
scripts that should help to understand the basics of yade. `/sinkhole_model` contains
contains two scripts to demonstrate a simple sinkhole model
### `/data`
No files in this folder are committed to git. It should contain 
any files created by a yade script (Specific element-ensembles or
trajectory files for postprocessing)
### `/docker`
dockerfile to compile yade in a docker container. It installs all
dependencies do compile yade. If you install yade as package (see yade doc)
you would not need this

## Installation

To install yade on a ubuntu system follow the instructions on 
[yadehomepage](https://yade-dem.org/doc/installation.html).
If you want/need to compile yade on your own machine
i would recommend to use a docker container. You could use 
`docker/dockerfile` for that.

## Understanding Yade


### About the example: "gravity deposition"

#### FAQ

* What is WallMask in geom.facetBox?
	* wallMask (bitmask) – determines which walls will be created, in the order -x (1), +x (2), -y (4), +y (8), -z (16), +z (32). The numbers are ANDed; the default 63 means to create all walls
	* see [documentation](https://yade-dem.org/doc/yade.geom.html)

* What is a ForceResetter() 
	* A Class that will Reset all forces stored in Scene::forces (O.forces in python). Typically, this is the first engine to be run at every step. In addition, reset those energies that should be reset, if energy tracing is enabled.
* What is a InsertionSortCollider()?
	* It is a special kind of Collider using Insertion Sort to gain a complexity of $O(n \log(n))$ complexity using Aabb (Axis-aligned bounding box) for bounds. [docu](https://yade-dem.org/doc/yade.wrapper.html#yade.wrapper.InsertionSortCollider)

* What is a Collider?
	* [docu](https://yade-dem.org/doc/yade.wrapper.html#yade.wrapper.Collider)

* What is an Aabb (Axis-aligned bounding box)?
	* It is a box around a given object. To check if to objects collide, it is first checked if those boxes are touching, if yes a IGeomFunctor checks if the more complicated object collide.

* What is an InteractionLoop()?
	* 

* What is vnoremap <C-c> "
