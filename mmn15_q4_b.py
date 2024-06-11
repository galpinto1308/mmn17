"""
This program is animating a cube that rotate around its axis
In this program the users can choose between Perspective and Orthographic projections via a keyboard input.
O - Orthographic (And default)
P - Perspective
y
"""


from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import sys
import os

# init window size
width = 700
height = 700
rotate_angle = 0
orthographic_projection = True
font = GLUT_BITMAP_TIMES_ROMAN_24
font_width = 11
font_height = 35
text = "To change the projection mode:"
second_text = "Hit on the keyboard - P for Perspective or O for Orthographic"


# myRespahe function to be called when the user resize the window
def myReshape(w, h):
    global width, height
    width = w
    height = h
# myKeyBoard function to be called when the user hit the keyboard
def myKeyboard(key, x, y):
    global orthographic_projection
    if key.lower() == b'o':
        orthographic_projection = True
    elif key.lower() == b'p':
        orthographic_projection = False

# myDisplay function to be called  when drawing in the window
def myDisplay():
    global width, height, rotate_angle, orthographic_projection
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    drawText()

    if orthographic_projection:
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-70,70,-70 ,70,25,180)  # orthographic projection
        glViewport(0, 0, width, height)
        glColor3f(1, 0, 0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(100, 60, 50, 10, 10, 0, 0, 1, 0)  # camera position
        glRotate(rotate_angle, 0, 1, 0)  # rotation in 1 degree each time creates the animation
        glutSolidCube(30)  # drawing the solid cube
        # drawing black wired cube for prettify the object
        glColor3f(0, 0, 0)
        glEnable(GL_LINE_SMOOTH)
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glutWireCube(30)
    else:
        # Set up the projection matrix
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glFrustum(-70, 70, -70, 70, 25, 180)  # Perspective projection
        # Set up the viewport
        glViewport(0, 0, width, height)
        # Switch to the modelview matrix
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(100, 60, 50, 40, 40, 0, 0, 1, 0)  # Camera setup
        # Set the color for drawing
        glColor3f(1, 0, 0)
        glRotate(rotate_angle, 0, 1, 0)  # rotation in 1 degree each time creates the animation
        glutSolidCube(70)  # drawing the solid cube
        # drawing black wired cube for prettify the object
        glColor3f(0, 0, 0)
        glEnable(GL_LINE_SMOOTH)
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glutWireCube(70)


    glutSwapBuffers()
    rotate_angle += 1
# method for drawing the instruction to the user
def drawText():
    text_width = max(len(text),len(second_text)) * font_width  # the width that will contain both titles
    viewport_x = glutGet(GLUT_WINDOW_WIDTH) - text_width
    viewport_y = glutGet(GLUT_WINDOW_HEIGHT) - 2 * font_height
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, text_width, 0, 2 * font_height)
    # creating viewport for inserting the text
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glViewport(viewport_x, viewport_y, text_width, 2 * font_height)
    glColor3f(0, 0, 0) # text color - black
    # drawing the text
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glRasterPos2f(0,font_height)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    glRasterPos2f(0, 0)
    for ch in second_text:
        glutBitmapCharacter(font, ord(ch))
    glDisable(GL_BLEND)
# call this function each 30 ms to rotate the object
def animate(_):
    glutPostRedisplay()   # calling the myDisplay function again
    glutTimerFunc(30, animate,0)

# main to initialize the window size and start the main loop of the graphic
def main():
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
        glutInitWindowSize(width, height)
        glutInitWindowPosition(0, 0)
        glutCreateWindow("MMN 15_q4_b")
        glEnable(GL_DEPTH_TEST)
        glutDisplayFunc(myDisplay)
        glutReshapeFunc(myReshape)
        glutKeyboardFunc(myKeyboard)
        glClearColor(1, 1, 1, 1)  # background color - White
        glutTimerFunc(30, animate, 0)
        glutMainLoop()

if __name__ == "__main__":
    main()