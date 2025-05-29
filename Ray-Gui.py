import streamlit as st
import textwrap

st.set_page_config(page_title="Raysect Explorer", layout="wide")

st.title("🔬 Raysect Interactive Explorer")
st.markdown("Explore core functionalities of Raysect through interactive examples.")

# Define code snippets for different functionalities
examples = {
    "Define a Light Source": {
        "description": "Create an emitting box using UniformSurfaceEmitter.",
        "code": '''
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
'''
    },
    "Apply a Material": {
        "description": "Apply a Lambertian material to a sphere.",
        "code": '''
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
'''
    },
    "Set Up an Observer": {
        "description": "Configure a pinhole camera to observe the scene.",
        "code": '''
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
'''
    },
    "Combine Elements": {
        "description": "Combine source, material, and observer in a single scene.",
        "code": '''
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
}

# Sidebar for selection
st.sidebar.title("Select Functionality")
selection = st.sidebar.radio("Choose an example:", list(examples.keys()))

# Display selected example
st.subheader(selection)
st.markdown(examples[selection]["description"])
st.code(textwrap.dedent(examples[selection]["code"]), language='python')

st.markdown("---")
st.markdown("For more detailed information, visit the [Raysect Documentation](https://www.raysect.org/).")
