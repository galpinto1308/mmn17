import OpenGL
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from math import *
import sys
import os

# Global variables for camera rotation
camera_angle_x = 0.0
camera_angle_y = 0.0
camera_distance = 6.0

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

shoulder_angle = 0
elbow_angle = 0

def draw_cube():
    glutSolidCube(1.0)

def draw_prism():
    glBegin(GL_QUADS)
    # Front face
    glVertex3f(-0.5, -0.5,  0.5)
    glVertex3f( 0.5, -0.5,  0.5)
    glVertex3f( 0.5,  0.5,  0.5)
    glVertex3f(-0.5,  0.5,  0.5)
    # Back face
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f( 0.5, -0.5, -0.5)
    glVertex3f( 0.5,  0.5, -0.5)
    glVertex3f(-0.5,  0.5, -0.5)
    # Top face
    glVertex3f(-0.5,  0.5, -0.5)
    glVertex3f( 0.5,  0.5, -0.5)
    glVertex3f( 0.5,  0.5,  0.5)
    glVertex3f(-0.5,  0.5,  0.5)
    # Bottom face
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f( 0.5, -0.5, -0.5)
    glVertex3f( 0.5, -0.5,  0.5)
    glVertex3f(-0.5, -0.5,  0.5)
    # Right face
    glVertex3f( 0.5, -0.5, -0.5)
    glVertex3f( 0.5,  0.5, -0.5)
    glVertex3f( 0.5,  0.5,  0.5)
    glVertex3f( 0.5, -0.5,  0.5)
    # Left face
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(-0.5,  0.5, -0.5)
    glVertex3f(-0.5,  0.5,  0.5)
    glVertex3f(-0.5, -0.5,  0.5)
    glEnd()

def draw_sphere(radius):
    quadric = gluNewQuadric()
    gluSphere(quadric, radius, 20, 20)
    gluDeleteQuadric(quadric)

def draw_claw():

    glTranslatef(0, -0.65, 0.0)
    glColor3f(0.1, 0.0, 0.0)
    glPushMatrix()
    glScalef(1.3, 1, 0.6)
    draw_sphere(0.5)
    glPopMatrix()
    glColor3f(1, 0.0, 0.0)

    # Draw the first prism
    glTranslatef(0.0, -1.5, 0.0)
    glPushMatrix()
    glTranslatef(-0.5, 0.0, 0.0)
    glRotatef(-45, 0.0, 0.0, 1.0)
    glScalef(1.0, 2.0, 0.5)
    draw_prism()
    glPopMatrix()

    # Draw the second prism
    glPushMatrix()
    glTranslatef(0.5, 0.0, 0.0)
    glRotatef(45, 0.0, 0.0, 1.0)
    glScalef(1.0, 2.0, 0.5)
    draw_prism()
    glPopMatrix()

def draw_arm():
    global shoulder_angle, elbow_angle

    # Draw the shoulder
    glPushMatrix()
    glRotatef(shoulder_angle, 1.0, 0.0, 0.0)
    glTranslatef(-0.8, 0, 0.0)
    glPushMatrix()
    glScalef(0.5, 0.5, 0.5)  # Scale to make a rectangular shape
    draw_cube()
    glPopMatrix()

    # Draw the elbow
    glTranslatef(0.0, -0.5, 0.0)
    glRotatef(elbow_angle, 1.0, 0.0, 0.0)
    glPushMatrix()
    glScalef(0.5, 1.0, 0.5)  # Scale to make a rectangular shape
    draw_cube()
    glPopMatrix()

    # Draw the hand (claw)
    glPushMatrix()
    glTranslatef(-0.1, -0.45, 0.0)
    glScalef(0.15, 0.15, 0.3)
    draw_claw()
    glPopMatrix()

    glPopMatrix()


def draw_body():
    glTranslatef(0.0, 0.25, 0.0)
    glRotatef(90, 1, 0, 0)
    glScalef(1.3, 1.1, 1.75)

    # Create a quadric object
    quadric = gluNewQuadric()
    gluQuadricNormals(quadric, GLU_SMOOTH)

    # Draw the cylinder
    gluCylinder(quadric, 0.5, 0.5, 1.0, 20, 20)

    # Draw the bottom cap
    glPushMatrix()
    glTranslatef(0.0, 0.0, 0.0)  # move to the bottom
    gluDisk(quadric, 0.0, 0.5, 20, 1)
    glPopMatrix()

    # Draw the top cap
    glPushMatrix()
    glTranslatef(0.0, 0.0, 1.0)  # move to the top
    gluDisk(quadric, 0.0, 0.5, 20, 1)
    glPopMatrix()

    # Delete the quadric object
    gluDeleteQuadric(quadric)


def draw_head_features():
    # Draw eyes, nose, mouth relative to the cube's transformations
    # Eyes
    # Apply scaling to make the cube a rectangular cuboid
    glScalef(2.0, 1.0, 1.0)  # Scale x by 2, y and z remain the same
    glColor3f(1.0, 0.0, 0.0)
    # Draw the solid cube
    glutSolidCube(0.5)
    glEnable(GL_BLEND)  # Enable blending, which is required for smoothing
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # Set blend function
    glEnable(GL_LINE_SMOOTH)  # Enable line smoothing
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)  # Optional: ask for the nicest line smoothing
    glLineWidth(1.5)  # Optional: set line width to make it slightly thicker
    glutWireCube(0.5)

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


def draw_robot():
    glPushMatrix()
    glColor3f(1.0, 0.0, 0.0)  # Red color

    glPushMatrix()
    glTranslatef(0, 0.58, 0)
    glScalef(1, 1.2, 1)
    draw_head_features()
    glPopMatrix()

    glColor3f(1.0, 0.0, 0.0)

    # Body (cylinder)
    glPushMatrix()
    draw_body()
    glPopMatrix()

    glPushMatrix()
    draw_arm()
    glPopMatrix()

    glPushMatrix()
    glScalef(-1, 1, 1)
    draw_arm()
    glPopMatrix()

    # Legs (cubes)
    glPushMatrix()
    glTranslatef(0.3, -2.0, 0.0)
    glScalef(0.5, 1.0, 0.5)  # Scale down and elongate the cube
    draw_cube()
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-0.3, -2.0, 0.0)
    glScalef(0.5, 1.0, 0.5)  # Scale down and elongate the cube
    draw_cube()
    glPopMatrix()

    glPopMatrix()

def myDisplay():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Clear the color buffer and the depth buffer
    glLoadIdentity()
    # Set camera position and orientation
    gluLookAt(camera_distance * sin(camera_angle_y * pi / 180.0) * cos(camera_angle_x * pi / 180.0),
              camera_distance * sin(camera_angle_x * pi / 180.0),
              camera_distance * cos(camera_angle_y * pi / 180.0) * cos(camera_angle_x * pi / 180.0),
              0, 0, 0, 0, 1, 0)

    draw_robot()

    glutSwapBuffers()
    glFlush()

def special_key_pressed(key, x, y):
    global camera_angle_x, camera_angle_y, camera_distance

    # Adjust camera angles and distance based on arrow key pressed
    if key == GLUT_KEY_UP:
        camera_angle_x += 5.0
    elif key == GLUT_KEY_DOWN:
        camera_angle_x -= 5.0
    elif key == GLUT_KEY_LEFT:
        camera_angle_y -= 5.0
    elif key == GLUT_KEY_RIGHT:
        camera_angle_y += 5.0

    # Clamp camera angle within reasonable limits
    camera_angle_x = max(-90.0, min(90.0, camera_angle_x))
    camera_angle_y %= 360.0

    glutPostRedisplay()

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
    glutSpecialFunc(special_key_pressed)
    glutReshapeFunc(myReshape)
    glutMainLoop()


if __name__ == "__main__":
    main()
