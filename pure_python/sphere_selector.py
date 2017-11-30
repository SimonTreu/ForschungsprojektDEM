import numpy as np

def select_spheres_in_circle_on_plane(spheres, center, radius):

    center = np.array(center)

    spheres_inside_bsphere = []
    spheres_outside_bsphere = []

    while len(spheres) > 0:
        s = spheres.pop()
        c = np.array(s.state.pos)
        c -= center
        if np.linalg.norm(c) <= radius:
            spheres_inside_bsphere.append(s)
        else:
            spheres_outside_bsphere.append(s)

    return spheres_inside_bsphere, spheres_outside_bsphere
