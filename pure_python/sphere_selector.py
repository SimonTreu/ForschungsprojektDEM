import numpy as np

def select_spheres_in_circle_on_plane(spheres, center, radius):

    center = np.array(center)
    selected_spheres = []

    for s in spheres:
        c = np.array(s.state.pos)
        c -= center
        if np.linalg.norm(c) <= radius:
            selected_spheres.append(s)

    return selected_spheres
