from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


def init():
    glClearColor(0.8, 0.8, 0.8, 1)  # Set the background color
    glEnable(GL_DEPTH_TEST)  # Enable depth testing


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(5, 3, 5, 0, -15, 0, 0, 1, 0)  # Set camera position

    draw_checkerboard()

    glutSwapBuffers()


def draw_checkerboard():
    size = 2  # Size of each square
    rows = 100  # Number of rows
    columns = 100  # Number of columns

    for row in range(rows):
        for col in range(columns):
            if (row + col) % 2 == 0:
                glColor3f(1, 1, 1)  # White
            else:
                glColor3f(0, 0, 0)  # Black

            glBegin(GL_QUADS)
            glVertex3f(col * size, 0, row * size)
            glVertex3f(col * size, 0, (row + 1) * size)
            glVertex3f((col + 1) * size, 0, (row + 1) * size)
            glVertex3f((col + 1) * size, 0, row * size)
            glEnd()


def reshape(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, float(w) / float(h), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)


def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(640, 480)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"OpenGL Checkerboard")
    init()
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutMainLoop()


if __name__ == "__main__":
    main()
