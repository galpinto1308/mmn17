from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from math import *
import sys

import robot
from robot import *
from floor import *
from furniture import *

# Global variables for camera rotation
camera_angle_x = 0.0
camera_angle_y = 0.0
camera_distance = 6.0

ambient_factor = 0.9
move_flag = 0


def myDisplay():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Clear the color buffer and the depth buffer
    glLoadIdentity()
    # Set camera position and orientation
    gluLookAt(camera_distance * sin(camera_angle_y * pi / 180.0) * cos(camera_angle_x * pi / 180.0),
              camera_distance * sin(camera_angle_x * pi / 180.0),
              camera_distance * cos(camera_angle_y * pi / 180.0) * cos(camera_angle_x * pi / 180.0),
              0, 0, 0, 0, 1, 0)

    lighting()
    draw_checkerboard()
    draw_robot()
    draw_table()
    draw_tresh_can()

    glutSwapBuffers()
    glFlush()


# myRespahe function to be called when the user resize the window
def myReshape(width, height):
    if height == 0:
        height = 1  # Prevent divide by zero
    aspect = width / height

    glViewport(0, 0, width, height)

    glMatrixMode(GL_PROJECTION)  # To operate on the Projection matrix
    glLoadIdentity()  # Reset the projection matrix
    gluPerspective(45.0, aspect, 0.1, 100.0)

    glMatrixMode(GL_MODELVIEW)  # To operate on the model-view matrix
    glLoadIdentity()  # Reset the model-view matrix


def lighting():
    glEnable(GL_LIGHTING)  # Enable lighting

    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
    # Light model parameters:
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [ambient_factor, ambient_factor, ambient_factor, 1])  # Ambient light

    """
    # Spotlight properties
    light_position = [0, 0, 6, 1.0]  # Spotlight position
    light_direction = [0, 0, -1]  # The direction vector pointing downwards
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, light_direction)
    glLightfv(GL_LIGHT0, GL_SPOT_CUTOFF, 45.0)  # Beam width
    glLightfv(GL_LIGHT0, GL_SPOT_EXPONENT, 2)  # Focus strength

    # Define light intensity
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1, 1, 1, 1.0])  # White diffuse light
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])  # White specular light
    """
def arrows_key_pressed(key, x, y):
    global camera_angle_x, camera_angle_y, camera_distance, move_flag, ambient_factor

    # Adjust camera angles and distance based on arrow key pressed
    if key == GLUT_KEY_UP:
        if move_flag == 9:
            if ambient_factor <= 1:
                ambient_factor += 0.05
        elif move_flag == 0:
            camera_angle_x += 5.0
    elif key == GLUT_KEY_DOWN:
        if move_flag == 9:
            if ambient_factor >= 0:
                ambient_factor -= 0.05
        elif move_flag == 0:
            camera_angle_x -= 5.0
    elif key == GLUT_KEY_LEFT:
        if move_flag == 0:
            camera_angle_y -= 5.0
        elif move_flag == 1:
            robot.head_angle -= 5.0
    elif key == GLUT_KEY_RIGHT:
        if move_flag == 0:
            camera_angle_y += 5.0
        elif move_flag == 1:
            robot.head_angle += 5.0

    # Clamp camera angle within reasonable limits
    camera_angle_x = max(-90.0, min(90.0, camera_angle_x))
    camera_angle_y %= 360.0

    glutPostRedisplay()

def key_pressed(key, x, y):
    global move_flag
    move_flag = int(key)

# main to initialize the window size and start the main loop of the graphic
def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(700, 700)
    glutInitWindowPosition(0, 0)
    glutCreateWindow("MMN 17")
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glShadeModel(GL_SMOOTH)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
    glutDisplayFunc(myDisplay)
    glutSpecialFunc(arrows_key_pressed)
    glutKeyboardFunc(key_pressed)
    glutReshapeFunc(myReshape)
    glutMainLoop()


if __name__ == "__main__":
    main()
