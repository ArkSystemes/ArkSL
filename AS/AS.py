import numpy as np
import imageio
import vedo

# Paramètres de la vidéo
width, height = 640, 480
fps = 30
duration = 2  # en secondes
n_frames = fps * duration

# Créez le torus (cercle 3D)
torus = vedo.Torus(r=0.3, R=1, c="lime", alpha=1)

# Créez la scène, la caméra et l'éclairage
scene = vedo.Plotter(offscreen=True, axes=0, bg="white")
scene.add(torus)
scene.add(vedo.Light("white", pos=[5, 5, 5], deg=30))
scene.camera.SetPosition([5, 5, 5])
scene.camera.SetFocalPoint([0, 0, 0])
scene.camera.SetViewUp([0, 1, 0])

# Fonction pour mettre à jour la rotation du torus et rendre une image
def render_frame(rotation_x):
    torus.rotate(rotation_x, axis=[1, 0, 0], point=[0, 0, 0])
    return scene.getScreenshot()

# Créez la vidéo
with imageio.get_writer('torus_rotation.mp4', mode='I', fps=fps) as writer:
    for i in range(n_frames):
        rotation_x = 2 * np.pi * i / n_frames
        frame = render_frame(rotation_x)
        writer.append_data(frame)

scene.close()

