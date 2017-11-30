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

    spheres_in_bsphere = [spheres[i] for i in [1, 3, 4, 5, 7]]
    spheres_outside_bsphere = [spheres[i] for i in [0,2,6,8]]
    m_spheres_in_bsphere, m_spheres_outside_bsphere = select_spheres_in_circle_on_plane(spheres=spheres, center=(0,0,z), radius=1.5)
    assert set(m_spheres_in_bsphere) == set(spheres_in_bsphere)
    assert set(m_spheres_outside_bsphere) == set(spheres_outside_bsphere)

def test_selects_spheres_in_circle_not_at_center():
    z = 0
    radius = .5

    centers = [(-1.5, -1.5, z), (-1.5, 0, z), (-1.5, 1.5, z),
               (0, -1.5, z), (0, 0, z), (0, 1.5, z),
               (1.5, -1.5, z), (1.5, 0, z), (1.5, 1.5, z)]
    spheres = []

    for c in centers:
        spheres.append(sphere(center=c, radius=radius, fixed=True))

    spheres_in_bsphere = [spheres[i] for i in [4, 6, 7, 8]]
    spheres_outside_bsphere = [spheres[i] for i in [0, 1, 2, 3, 5]]

    m_spheres_in_bsphere, m_spheres_outside_bsphere = select_spheres_in_circle_on_plane(spheres=spheres,
                                                            center=(1.5, 0, z), radius=1.5)

    assert set(m_spheres_in_bsphere) == set(spheres_in_bsphere)
    assert set(m_spheres_outside_bsphere) == set(spheres_outside_bsphere)
