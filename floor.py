from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

def draw_checkerboard():
    glPushMatrix()
    glNormal3f(0, 1, 0)

    size = 2
    rows = 100
    columns = 100

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