from sphere_selector import *
from yadeimport import *
def test_selects_spheres_in_circle():
    z = 0
    radius = .5

    centers = [(-1.5, -1.5, z), (-1.5, 0, z), (-1.5, 1.5, z),
               (0, -1.5, z), (0, 0, z), (0, 1.5, z),
               (1.5, -1.5, z), (1.5, 0, z), (1.5, 1.5, z)]
    spheres = []

    for c in centers:
        spheres.append(sphere(center=c, radius=radius, fixed=True))

    spheres_in_circle = [spheres[i] for i in [1, 3, 4, 5, 7]]
    m_spheres_in_cirlce = select_spheres_in_circle_on_plane(spheres=spheres, center=(0,0,z), radius=1.5)
    assert set(m_spheres_in_cirlce) == set(spheres_in_circle)

def test_selects_spheres_in_circle_not_at_center():
    z = 0
    radius = .5

    centers = [(-1.5, -1.5, z), (-1.5, 0, z), (-1.5, 1.5, z),
               (0, -1.5, z), (0, 0, z), (0, 1.5, z),
               (1.5, -1.5, z), (1.5, 0, z), (1.5, 1.5, z)]
    spheres = []

    for c in centers:
        spheres.append(sphere(center=c, radius=radius, fixed=True))

    spheres_in_circle = [spheres[i] for i in [4, 6, 7, 8]]

    m_spheres_in_cirlce = select_spheres_in_circle_on_plane(spheres=spheres,
                                                            center=(1.5,0,z), radius=1.5)

    assert set(m_spheres_in_cirlce) == set(spheres_in_circle)
