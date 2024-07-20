from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GLUT.freeglut import *
import sys
width, height = 800, 600


def create_eye_list():
    eye_list = glGenLists(1)
    glNewList(eye_list, GL_COMPILE)
    glColor3f(0, 0, 0)  # Black color for the eyes
    glutSolidSphere(0.05, 32, 32)  # Eye sphere
    glEndList()
    return eye_list


def create_nose_list():
    nose_list = glGenLists(1)
    glNewList(nose_list, GL_COMPILE)
    glBegin(GL_TRIANGLES)
    glVertex3f(-0.025, 0, 0)
    glVertex3f(0.025, 0, 0)
    glVertex3f(0, 0.05, 0)
    glEnd()
    glEndList()
    return nose_list


def create_mouth_list():
    mouth_list = glGenLists(1)
    glNewList(mouth_list, GL_COMPILE)
    glBegin(GL_QUADS)
    glVertex3f(-0.075 / 2, -0.1, 0.26)
    glVertex3f(0.075 / 2, -0.1, 0.26)
    glVertex3f(0.075 / 2, -0.15, 0.26)
    glVertex3f(-0.075 / 2, -0.15, 0.26)
    glEnd()
    glEndList()
    return mouth_list

def create_head_list():
    head_list = glGenLists(1)
    glNewList(head_list, GL_COMPILE)
    glScalef(2.0, 1.0, 1.0)  # Scale x by 2, y and z remain the same
    glColor3f(0, 0, 1)
    glutSolidCube(0.5)
    glColor3f(0, 0, 0)
    glEnable(GL_BLEND)  # Enable blending, which is required for smoothing
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # Set blend function
    glEnable(GL_LINE_SMOOTH)  # Enable line smoothing
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)  # Optional: ask for the nicest line smoothing
    glLineWidth(1.5)  # Optional: set line width to make it slightly thicker
    glutWireCube(0.5)
    glEndList()
    return head_list


def create_head(head_list, eye_list, nose_list, mouth_list):
    head = glGenLists(1)
    glNewList(head,GL_COMPILE)
    # head
    glCallList(head_list)
    # Eyes
    glPushMatrix()
    glTranslatef(-0.1, 0.12, 0.26)
    glCallList(eye_list)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.1, 0.12, 0.26)
    glCallList(eye_list)
    glPopMatrix()

    # Nose
    glPushMatrix()
    glTranslatef(0, 0, 0.26)
    glCallList(nose_list)
    glPopMatrix()

    # Mouth
    glPushMatrix()
    glScalef(2.0, 1.0, 1.0)  # Match scaling to the cube's scaling
    glCallList(mouth_list)
    glPopMatrix()

    glEndList()
    return head


def draw_scene():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(2, 0, 2, 0, 0, 0, 0, 1, 0)
    eye_list = create_eye_list()
    nose_list = create_nose_list()
    mouth_list = create_mouth_list()
    head_list = create_head_list()
    temp = create_head(head_list, eye_list, nose_list, mouth_list)
    glCallList(temp)
    glutSwapBuffers()
def reshape(w, h):

    glViewport(0, 0, w, h)

    # Switch to the projection matrix
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    # Set up a perspective projection matrix
    gluPerspective(45.0, float(w) / float(h), 1.0, 100.0)

    # Switch back to the modelview matrix
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(width, height)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Solid Blue Rectangular Cuboid with Robot Face")

    # Enable depth testing for correct rendering of overlapping objects
    glEnable(GL_DEPTH_TEST)

    # Set the display callback function to draw the cube
    glutDisplayFunc(draw_scene)

    # Set the reshape callback function to handle window resizing
    glutReshapeFunc(reshape)

    # Set the background color to white
    glClearColor(1, 1, 1, 1)

    # Enter the GLUT event processing loop
    glutMainLoop()


if __name__ == "__main__":
    main()
