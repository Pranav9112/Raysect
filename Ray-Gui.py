import streamlit as st
import textwrap

st.set_page_config(page_title="Raysect Interactive Explorer", layout="wide")

st.markdown("""
<style>
section[data-testid='stSidebar'] {
    background-color: #f0f2f6;
}
</style>
""", unsafe_allow_html=True)

st.title("🔬 Raysect Interactive Explorer")

# Define code snippets for different functionalities
examples = {
    "Define a Light Source": '''
from raysect.primitive import Box
from raysect.optical import World, Point3D
from raysect.optical.material import UniformSurfaceEmitter
from raysect.optical.library import d65_white

world = World()

emitter = Box(
    lower=Point3D(-1, -1, 0),
    upper=Point3D(1, 1, 0.1),
    material=UniformSurfaceEmitter(d65_white, 1.0),
    parent=world
)
''',
    "Apply a Material": '''
from raysect.primitive import Sphere
from raysect.optical import World, translate
from raysect.optical.material import Lambert

world = World()

sphere = Sphere(
    radius=1.0,
    transform=translate(0, 0, 0),
    material=Lambert(),
    parent=world
)
''',
    "Set Up an Observer": '''
from raysect.optical.observer import PinholeCamera, RGBPipeline2D
from raysect.optical import World, translate

world = World()

rgb = RGBPipeline2D()

camera = PinholeCamera(
    parent=world,
    pipeline=rgb,
    fov=45,
    pixels=(512, 512),
    transform=translate(0, 0, -5)
)

camera.observe()
rgb.save("rendered_scene.png")
''',
    "Combine Elements": '''
from raysect.primitive import Sphere, Box
from raysect.optical import World, translate, Point3D
from raysect.optical.material import Lambert, UniformSurfaceEmitter
from raysect.optical.library import d65_white
from raysect.optical.observer import PinholeCamera, RGBPipeline2D

world = World()

# Emitting box
emitter = Box(
    lower=Point3D(-1, -1, 0),
    upper=Point3D(1, 1, 0.1),
    material=UniformSurfaceEmitter(d65_white, 1.0),
    parent=world
)

# Reflective sphere
sphere = Sphere(
    radius=1.0,
    transform=translate(0, 0, 2),
    material=Lambert(),
    parent=world
)

# Camera setup
rgb = RGBPipeline2D()

camera = PinholeCamera(
    parent=world,
    pipeline=rgb,
    fov=45,
    pixels=(512, 512),
    transform=translate(0, 0, -5)
)

camera.observe()
rgb.save("combined_scene.png")
'''
}

st.sidebar.title("Toolbox")

# Render buttons for each example
for label in examples.keys():
    if st.sidebar.button(label):
        with st.container():
            st.subheader(label)
            st.code(textwrap.dedent(examples[label]), language='python')

st.markdown("---")
st.markdown("Visit the [Raysect Documentation](https://www.raysect.org/) for deeper info.")
