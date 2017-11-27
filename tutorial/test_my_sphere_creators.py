from my_sphere_creators import *

def test_create_fixed_boundary_spheres():
    x_range = [-1.5,1.5]
    y_range = [-1.5,1.5]
    z = 0
    radius = .5

    center = [(-1.5,-1.5,0),(-1.5,0,0),(-1.5,1.5,0),
              (0,-1.5,0),(0,0,0),(0,1.5,0),
              (1.5,-1.5,0),(1.5,0,0),(1.5,1.5,0)]
    distance = 2*radius + .5
    creator = FixedBoundarySpheresCreator(x_range,y_range,z)
    assert creator.create_centers(distance) == center

def test_create_fixed_boundary_spheres_no_square():
    x_range = [-1.5,1.5]
    y_range = [-1.5,0]
    z = 0
    radius = .5
    distance = 2 * radius + .5

    center = [(-1.5,-1.5,0),(-1.5,0,0),
              (0,-1.5,0),(0,0,0),
              (1.5,-1.5,0),(1.5,0,0)]

    creator = FixedBoundarySpheresCreator(x_range, y_range, z)
    assert creator.create_centers(distance) == center

def test_create_spheres():
    x_range = [-1.5, 1.5]
    y_range = [-1.5, 1.5]
    z = 0
    radius = .5

    center = [(-1.5, -1.5, 0), (-1.5, 0, 0), (-1.5, 1.5, 0),
              (0, -1.5, 0), (0, 0, 0), (0, 1.5, 0),
              (1.5, -1.5, 0), (1.5, 0, 0), (1.5, 1.5, 0)]
    distance = 2 * radius + .5
    creator = FixedBoundarySpheresCreator(x_range, y_range, z)
    centers = creator.create_centers(distance)
    spheres = creator.create_spheres(centers, radius)

    assert len(spheres) == 9

