from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GLUT.freeglut import *
import sys

# Set initial window size
width, height = 800, 600




def draw_features():
    # Draw eyes, nose, mouth relative to the cube's transformations
    # Eyes
    glColor3f(0, 0, 0)  # Black color for the eyes
    glPushMatrix()
    glTranslatef(-0.1, 0.12, 0.26)  # Adjust the position so it is relative to cube size
    glutSolidSphere(0.05, 32, 32)  # Use solid spheres for 3D eyes
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.1, 0.12, 0.26)
    glutSolidSphere(0.05, 32, 32)
    glPopMatrix()

    # Nose
    glPushMatrix()
    glTranslatef(0, 0, 0.26)
    glBegin(GL_TRIANGLES)
    glVertex3f(-0.025, 0, 0)
    glVertex3f(0.025, 0, 0)
    glVertex3f(0, 0.05, 0)
    glEnd()
    glPopMatrix()

    # Mouth - Adjust the position and dimensions to ensure it's centered on the scaled cuboid
    glPushMatrix()  # Apply the same scale as the cube to ensure correct positioning
    glScalef(2.0, 1.0, 1.0)  # Match scaling to the cube's scaling
    glBegin(GL_QUADS)
    glVertex3f(-0.075 / 2, -0.1, 0.26)  # Adjust the x-coordinates to compensate for scaling
    glVertex3f(0.075 / 2, -0.1, 0.26)
    glVertex3f(0.075 / 2, -0.15, 0.26)
    glVertex3f(-0.075 / 2, -0.15, 0.26)
    glEnd()
    glPopMatrix()

def draw_cube():
    global width, height
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Adjust camera for semi-profile view
    gluLookAt(2, 0, 2, 0, 0, 0, 0, 1, 0)

    # Apply scaling to make the cube a rectangular cuboid
    glScalef(2.0, 1.0, 1.0)  # Scale x by 2, y and z remain the same

    # Draw the solid cube
    glColor3f(0, 0, 1)
    glutSolidCube(0.5)
    glColor3f(0, 0, 0)
    glEnable(GL_BLEND)  # Enable blending, which is required for smoothing
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # Set blend function
    glEnable(GL_LINE_SMOOTH)  # Enable line smoothing
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)  # Optional: ask for the nicest line smoothing
    glLineWidth(1.5)  # Optional: set line width to make it slightly thicker
    glutWireCube(0.5)

    # Draw features on the cube
    draw_features()
    # Swap buffers
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
    glutDisplayFunc(draw_cube)

    # Set the reshape callback function to handle window resizing
    glutReshapeFunc(reshape)

    # Set the background color to white
    glClearColor(1, 1, 1, 1)

    # Enter the GLUT event processing loop
    glutMainLoop()


if __name__ == "__main__":
    main()