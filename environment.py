from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from obb import OBB
import numpy as np

size = 2
rows = 60
columns = 60
wall_height = 8.0


def draw_checkerboard():
    glPushMatrix()
    glNormal3f(0, 1, 0) 

    glTranslatef(-(rows / 2), -2.75, -(columns / 2))

    specular = [1.0, 1.0, 1.0, 1.0]
    shininess = 128.0

    glMaterialfv(GL_FRONT, GL_SPECULAR, specular)
    glMaterialf(GL_FRONT, GL_SHININESS, shininess)
    glBegin(GL_QUADS)
    for row in range(rows):
        for col in range(columns):
            if (row + col) % 2 == 0:
                glColor3f(1, 1, 1)
            else:
                glColor3f(0, 0, 0)

            glVertex3f(col * size, 0,  row * size)
            glVertex3f(col * size, 0, (row + 1) * size)
            glVertex3f((col + 1) * size, 0, (row + 1) * size)
            glVertex3f((col + 1) * size, 0, row * size)
    glEnd()
    glPopMatrix()  # Restore the original matrix
    

def draw_walls():
    glPushMatrix()
    glTranslatef(-(rows / 2), -2.75, -(columns / 2))

    glColor3f(0.6, 0.6, 0.6)  # Wall color

    # Left wall
    glBegin(GL_QUADS)
    glVertex3f(0, 0, 0)
    glVertex3f(0, wall_height, 0)
    glVertex3f(0, wall_height, columns * size)
    glVertex3f(0, 0, columns * size)
    glEnd()

    # Right wall
    glBegin(GL_QUADS)
    glVertex3f(rows * size, 0, 0)
    glVertex3f(rows * size, wall_height, 0)
    glVertex3f(rows * size, wall_height, columns * size)
    glVertex3f(rows * size, 0, columns * size)
    glEnd()

    # Front wall
    glBegin(GL_QUADS)
    glVertex3f(0, 0, 0)
    glVertex3f(0, wall_height, 0)
    glVertex3f(rows * size, wall_height, 0)
    glVertex3f(rows * size, 0, 0)
    glEnd()

    # Back wall
    glBegin(GL_QUADS)
    glVertex3f(0, 0, columns * size)
    glVertex3f(0, wall_height, columns * size)
    glVertex3f(rows * size, wall_height, columns * size)
    glVertex3f(rows * size, 0, columns * size)
    glEnd()

    glPopMatrix() 

def draw_wall_obbs():
    wall_obbs = []

    # Calculate wall positions and dimensions
    half_sizes_vertical = [0.1, wall_height / 2, (columns * size) / 2]
    half_sizes_horizontal = [(rows * size) / 2, wall_height / 2, 0.1]

    # Left wall
    left_wall_center = [-rows * size / 2, wall_height / 2 - 2.75, 0]
    left_wall_obb = OBB(left_wall_center, half_sizes_vertical, np.eye(3))
    wall_obbs.append(left_wall_obb)

    # Right wall
    right_wall_center = [rows * size / 2, wall_height / 2 - 2.75, 0]
    right_wall_obb = OBB(right_wall_center, half_sizes_vertical, np.eye(3))
    wall_obbs.append(right_wall_obb)

    # Front wall
    front_wall_center = [0, wall_height / 2 - 2.75, -columns * size / 2]
    front_wall_obb = OBB(front_wall_center, half_sizes_horizontal, np.eye(3))
    wall_obbs.append(front_wall_obb)

    # Back wall
    back_wall_center = [0, wall_height / 2 - 2.75, columns * size / 2]
    back_wall_obb = OBB(back_wall_center, half_sizes_horizontal, np.eye(3))
    wall_obbs.append(back_wall_obb)

    return wall_obbs
