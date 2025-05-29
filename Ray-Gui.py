import streamlit as st
from raysect.optical import World, Point3D, translate
from raysect.primitive import Box, Sphere, Plane
from raysect.optical.material import UniformSurfaceEmitter, Lambert
from raysect.optical.library import d65_white
from raysect.optical.observer import PinholeCamera, RGBPipeline2D
import matplotlib.pyplot as plt
import numpy as np

# Initialize session state
if 'world' not in st.session_state:
    st.session_state.world = World()
if 'rgb' not in st.session_state:
    st.session_state.rgb = None
if 'img' not in st.session_state:
    st.session_state.img = None

# Component logic
class LightSource:
    def __init__(self, width, height, radiance):
        self.width = width
        self.height = height
        self.radiance = radiance

    def apply(self):
        emitter = Box(
            lower=Point3D(-self.width/2, -self.height/2, 0),
            upper=Point3D(self.width/2, self.height/2, 0.1),
            material=UniformSurfaceEmitter(d65_white, self.radiance),
            parent=st.session_state.world
        )

class Material:
    def __init__(self, radius, reflectance):
        self.radius = radius
        self.reflectance = reflectance

    def apply(self):
        sphere = Sphere(
            radius=self.radius,
            transform=translate(0, 0, self.radius + 0.1),
            material=Lambert(self.reflectance, self.reflectance, self.reflectance),
            parent=st.session_state.world
        )

class Observer:
    def __init__(self, fov, width_px, height_px, distance):
        self.fov = fov
        self.width_px = width_px
        self.height_px = height_px
        self.distance = distance

    def apply(self):
        rgb = RGBPipeline2D()
        PinholeCamera(
            parent=st.session_state.world,
            pipeline=rgb,
            fov=self.fov,
            pixels=(self.width_px, self.height_px),
            transform=translate(0, 0, -self.distance)
        )
        st.session_state.rgb = rgb

# Render function
def render_scene(samples):
    with st.spinner("Rendering scene, please wait…"):
        st.session_state.rgb.render(ray_count=samples)
    img = np.clip(st.session_state.rgb.frame.buffer, 0, None)
    st.session_state.img = img
    st.image(img, caption="Rendered Scene", use_column_width=True)
    st.download_button("Download Image", data=img.tobytes(), file_name="render.raw")

# UI Layout
st.set_page_config(page_title="Raysect GUI Explorer", layout="wide")
st.title("🔬 Raysect GUI Explorer")

col1, col2 = st.columns([1, 3])

with col1:
    st.header("Controls")
    mode = st.radio("Select Option", ["Light Source", "Material", "Observer", "Render Scene"])

    if mode == "Light Source":
        width = st.number_input("Width (m)", 0.01, 5.0, 0.2)
        height = st.number_input("Height (m)", 0.01, 5.0, 0.2)
        radiance = st.number_input("Radiance (W/sr/m²/nm)", 0.1, 100.0, 1.0)
        if st.button("Add Light Source"):
            LightSource(width, height, radiance).apply()

    elif mode == "Material":
        radius = st.number_input("Sphere Radius (m)", 0.1, 5.0, 1.0)
        reflectance = st.slider("Reflectance", 0.0, 1.0, 0.8)
        if st.button("Add Material"):
            Material(radius, reflectance).apply()

    elif mode == "Observer":
        fov = st.slider("FOV (°)", 10, 120, 45)
        width_px = st.number_input("Image Width (px)", 100, 2048, 512)
        height_px = st.number_input("Image Height (px)", 100, 2048, 512)
        distance = st.number_input("Camera Distance (m)", 0.1, 10.0, 5.0)
        if st.button("Setup Observer"):
            Observer(fov, width_px, height_px, distance).apply()

    elif mode == "Render Scene":
        samples = st.number_input("Ray Samples", 100, 5000, 1000)
        if st.button("Render"):
            render_scene(samples)

with col2:
    st.header("Viewport")
    if st.session_state.img is not None:
        st.image(st.session_state.img, caption="Latest Render", use_column_width=True)
    else:
        st.write("No render yet. Configure the scene and click Render.")
