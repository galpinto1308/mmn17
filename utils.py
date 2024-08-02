from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
from PIL import Image

texture_ids = {}
def initialize_textures():
    global texture_ids
    images_to_load = ["textures/walls.jpg", "textures/wood.png", "textures/metal.jpg","textures/robot_texture.jpg"]
    texture_ids = {image: load_texture(image) for image in images_to_load}

def load_texture(image_name):
    img = Image.open(image_name)
    img_data = np.array(list(img.getdata()), np.uint8).reshape(img.size[1], img.size[0], 3)
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.width, img.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
    glBindTexture(GL_TEXTURE_2D, 0)
    return texture_id

def draw_cylinder(radius, height, slices, stacks):
    """ Draw a cylinder """
    glPushMatrix()
    quadric = gluNewQuadric()
    gluQuadricTexture(quadric, GL_TRUE)
    gluCylinder(quadric, radius, radius, height, slices, stacks)
    gluDeleteQuadric(quadric)
    glPopMatrix()

def draw_cube(size):
    """ Draw a Cube """
    half_size = size / 2.0  # Calculate half size to center the cube at the origin
    glBegin(GL_QUADS)
    # Front face
    glNormal3f(0.0, 0.0, 1.0)  # Normal pointing out of the front face
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-half_size, -half_size, half_size)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(half_size, -half_size, half_size)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(half_size, half_size, half_size)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-half_size, half_size, half_size)

    # Back face
    glNormal3f(0.0, 0.0, -1.0)  # Normal pointing out of the back face
    glTexCoord2f(1.0, 0.0)
    glVertex3f(-half_size, -half_size, -half_size)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(-half_size, half_size, -half_size)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(half_size, half_size, -half_size)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(half_size, -half_size, -half_size)

    # Top face
    glNormal3f(0.0, 1.0, 0.0)  # Normal pointing upwards
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-half_size, half_size, -half_size)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-half_size, half_size, half_size)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(half_size, half_size, half_size)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(half_size, half_size, -half_size)

    # Bottom face
    glNormal3f(0.0, -1.0, 0.0)  # Normal pointing downwards
    glTexCoord2f(1.0, 1.0)
    glVertex3f(-half_size, -half_size, -half_size)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(half_size, -half_size, -half_size)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(half_size, -half_size, half_size)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(-half_size, -half_size, half_size)

    # Right face
    glNormal3f(1.0, 0.0, 0.0)  # Normal pointing to the right
    glTexCoord2f(1.0, 0.0)
    glVertex3f(half_size, -half_size, -half_size)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(half_size, half_size, -half_size)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(half_size, half_size, half_size)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(half_size, -half_size, half_size)

    # Left face
    glNormal3f(-1.0, 0.0, 0.0)  # Normal pointing to the left
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-half_size, -half_size, -half_size)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(-half_size, -half_size, half_size)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(-half_size, half_size, half_size)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-half_size, half_size, -half_size)

    glEnd()
def draw_sphere(radius):
    """ Draw a Cube """
    quadric = gluNewQuadric()
    gluSphere(quadric, radius, 20, 20)
    gluDeleteQuadric(quadric)
