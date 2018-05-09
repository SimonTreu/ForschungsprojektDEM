# Protocol of the research project

## Project Structure

### `/source`
This folder contains all Yade scripts. In `/basic_examples` are 
scripts that should help to understand the basics of yade. `/sinkhole_model` contains two scripts to demonstrate a simple sinkhole model
### `/data`
No files in this folder are committed to git. It should contain 
any files created by a yade script (specific element-ensembles or
trajectory files for postprocessing)
### `/docker`
dockerfile to compile yade in a docker container. It installs all
dependencies do compile yade. It is also possible to install yade 
 without compiling it via the yadedaily package (see yade doc).

## Installation

To install yade on a ubuntu system follow the instructions on the 
[yadehomepage](https://yade-dem.org/doc/installation.html).
If you want/need to compile yade on your own machine
I would recommend to use a docker container. You could use 
`docker/dockerfile` for that.

## Understanding Yade

Yade is an implementation of the Discrete Element Method ([wikipedia](https://de.wikipedia.org/wiki/Diskrete-Elemente-Methode), 
[yade-docu](https://yade-dem.org/doc/formulation.html), [Cundall, Strack 1979](https://www.icevirtuallibrary.com/doi/10.1680/geot.1979.29.1.47)).
This method was developed to simulate the mechanical behaviour of a medium by describing it as a set of "discrete" or "distinct" elements and interaction
laws between such elements. It is also possible to apply body forces such as gravity that are independent of interactions. 
The most popular (due to computational simplicity) discrete elements are spheres. Any discrete element can have material
specific properties such as density and tension, which may change after an interaction.
A time step of a simulation consists of:

1. listing all interactions between particles (all particles that are within an interaction range of each other).
2. compute forces between interacting particles
3. apply body forces
4. use newtons 2nd law to compute resulting momentum.
5. update positions of particles
    
For numerical stability there is a upper bound for the size of a single time step `PWaveTimeStep()`


### External Documentation Sources

The documentation you are reading here is mainly based on documentation documents you can
find on the [yade website](https://yade-dem.org/doc/). To get an html document containing all
different documentation files go to [Full contents](https://yade-dem.org/doc/index-toctree.html).
That documentation is a good starting point to get an understanding of how to use Yade but it lacks 
descriptions as soon as you try to go beyond the basic examples and functions. 

As a good way of finding out how to do more difficult tasks (such as sinkhole simulations) I would recommend an iterative 
approach: 

1. Find related posts in the [forum](https://answers.launchpad.net/yade)
2. Check the documentation of mentioned functions (Quicksearch on the [yade website](https://yade-dem.org/doc/) works quite well for that)
3. Find publications where those functions are used (or even developed) in [yade related publications](https://yade-dem.org/doc/publications.html). 
4. Search the forum again for posts related to the functions you might want to use.
5. Check out [examples on github](https://github.com/yade/trunk/tree/master/examples).

### Basic Example

#### Basic Sphere

The file `source/basic_example/basic_sphere` is a minimalistic YADE script. The building blocks of 
a simulations are:

1. Add material properties for particles to simulation [as described here](https://yade-dem.org/doc/user.html#defining-materials)
    * if no material is defined,
    [default material properties](https://yade-dem.org/doc/yade.utils.html?highlight=defaultmaterial#yade.utils.defaultMaterial)
     are used for all particles.
    * if only one material is added it is used for all particles.
    * if multiple materials are added to the simulation they can be assigned to particles
    by an id, which is returned by `O.materials.append(...)` 
2. Define particles (here two spheres)
    * the module [utils](https://yade-dem.org/doc/yade.utils.html) contains 
    several helper functions to create particles of different shapes and types.
    The most commonly used one is the 
    [sphere creator](https://yade-dem.org/doc/yade.utils.html#yade.utils.sphere)
    *  to define fixed particles as boundary conditions, set `sphere(...,fixed=True,...)`. Such spheres don't move in space
    but behave otherwise normally with other particles.
3. Add the particles to the simulation. The static object O (Omega) contains all parameters of a simulation model. All 
    particles have to be appended to the O.bodies object.
4. Define simulation logic in the O.engines object. 
    * InsertionSortCollider() takes care of a first approximate interaction detection. `InsertionSortCollider([Bo1_Sphere_Aabb()])` dose that
    by checking if simple boxes containing the objects are overlapping. 
    * `InteractionLoop` is described [here](https://yade-dem.org/doc/introduction.html#interactions).
        * this loops over all interactions returned by the InsertionSortCollider(). 
    * `NewtonIntegrator` computes the momentum from all forces for each particle.
 5. `O.dt` sets the length of one timestep. For numerical stability it has to be a value that is smaller than PWaveTimeStep().
 
 ####  Sinkhole Model
 This model is an adaption of a model given in this [example on github](https://github.com/yade/trunk/tree/master/examples/jointedCohesiveFrictionalPM).
 The readme mentions several related publications 
 (Hartong2012a, Scholtes2012, Scholtes2013, Duriez2016 [see references](https://yade-dem.org/doc/publications.html))
 As those authors also implemented a lot of the used functions it is recommended to refer to those
 publications for a detailed explanation. The aim of this model is to implement a model that contains
 a box of fixed spheres as boundary condition. (only the side walls are fixed). A layer of cohesive
 material (i.e. solid rock) on the bottom that is held only by the fixed walls (the outer borders of the
 solid stone plate are fixed). The Box is filled with a loose material which has no cohesive forces.
 
 Every 0.1 second of virtual time a sphere from the center of the solid material is removed. After some 
 time parts of the solid material will break and free the loose material on top.
 
 ##### packing_in_cuboid.py
 
 Here we create a packing of spheres in a cuboid. A packing means that a given shape is filled with as many spheres as possible within a specific range of radii. This pack of spheres will be the bases for our model.
 it is saved in the /data directory with a filename starting with alignedBox. 
 This file can be used in a different simulation. With that method it is
 possible to base different kind of simulations on the same sphere packing
 or use different sphere packings for the same simulation.
 
 ##### sinkhole.py

The first important thing here is the definition of material properties. There is one material called
nonCohesiveMaterial for the loose spheres and one cohesive material for the spheres representing
solid stone. When the spheres are loaded from the packing created with `packing_in_cuboid.py` they are assigned do different
properties:

1. All spheres in the lower part of the cuboid are assigned with the cohesive material. This means they represent a solid stone.
2. All spheres in the upper part of the cuboid are assigned to the non cohesive material. This means they are free to move in space and don't stick together
3. The side walls are defined as fixed to give a boundary condition. 

After the initialization, the spheres in the middle of the lower part of the cuboid will not move, as they stick to the fixed side walls. 
So during the simulation some spheres from the center will be removed to create an instability. The spheres that will get removed during
the simulation are already selected in the initialization part.

    
        PyRunner(command='removeNextSphere()',  virtPeriod=0.1),

within the interaction loop arbitrarily removes one of those spheres for removal every 0.1 seconds
of virtual time (simulated time and not the real time the simulation takes).

The variable `interactionRadius` can be set to values larger than one. If you do so, then the initial
cohesive links will be also applied to particles that are close by and not only if they are touching.
Higher values of the `interactionRadius` correspond to a harder material. Please refer to 
[Scholtes2013](https://www.sciencedirect.com/science/article/pii/S0022509612002268) for further 
explanation of that method.

Cohesive links are only set up in the first step of the simulation. After that the interaction
detection factor (which made it possible to stick particles together that are not directly touching)
is reset to one. 

    O.step();
    #### initializes now the interaction detection factor to strictly 1
    ss2d3dg.interactionDetectionFactor = -1.
    is2aabb.aabbEnlargeFactor = -1.


#### VTK Recorder (saving trajectories)
    
It is possible to save trajectories of the simulation at some rate (for example every 500th iteration).
[yade docu](https://yade-dem.org/doc/yade.export.html). For a explanation on how to 
visualize such trajectories you may refer to the [official vtk website](https://www.vtk.org/)