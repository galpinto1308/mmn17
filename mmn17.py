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
head_angle = 0
move_flag = 0
# myRespahe function to be called when the user resize the window
def myReshape(width, height):
    if height == 0:
        height = 1  # Prevent divide by zero
    aspect = float(width) / float(height)

    glViewport(0, 0, width, height)

    glMatrixMode(GL_PROJECTION)  # To operate on the Projection matrix
    glLoadIdentity()  # Reset the projection matrix
    gluPerspective(45.0, aspect, 1, 100.0)

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

    glRotate(head_angle,0,1,0)
    glScalef(2.0, 1.0, 1.0)
    glColor3f(1.0, 0.0, 0.0)
    # head
    glutSolidCube(0.5)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_LINE_SMOOTH)
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
    glColor3f(0, 0, 0)
    glLineWidth(1.5)
    glutWireCube(0.5)

    # eyes
    glColor3f(0, 0, 0)
    glPushMatrix()
    glTranslatef(-0.1, 0.12, 0.26)
    glutSolidSphere(0.05, 32, 32)
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

    # Mouth
    glPushMatrix()
    glScalef(2.0, 1.0, 1.0)
    glBegin(GL_QUADS)
    glVertex3f(-0.075 / 2, -0.1, 0.26)
    glVertex3f(0.075 / 2, -0.1, 0.26)
    glVertex3f(0.075 / 2, -0.15, 0.26)
    glVertex3f(-0.075 / 2, -0.15, 0.26)
    glEnd()
    glPopMatrix()


def draw_robot():
    glPushMatrix()
    glColor3f(1.0, 0.0, 0.0)

    # placing of the robot in the scene
    glTranslatef(-1, 0, -1)
    glScalef(0.5, 0.5, 0.5)

    # head
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
def draw_checkerboard():
    glPushMatrix()
    glNormal3f(0, 1, 0)

    size = 2
    rows = 100
    columns = 100

    glTranslatef(-50, -2, -50)

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

def draw_table():
    # Table dimensions
    top_width = 2.0
    top_depth = 1.0
    top_height = 0.1
    leg_radius = 0.05
    leg_height = 1.0

    # place the table
    glPushMatrix()
    glTranslatef(1, 0, 0.5)
    glScalef(0.5, 0.5, 0.5)


    # draw the table base
    glPushMatrix()
    glColor3f(0.65, 0.32, 0.17)  # Brown color
    glScalef(top_width, top_height, top_depth)
    glutSolidCube(1)
    glPopMatrix()

    # Draw table legs
    glPushMatrix()
    glRotatef(90, 1, 0, 0)

    # first leg
    glPushMatrix()
    glTranslatef(- top_width/2 + leg_radius,-leg_radius,  0)
    draw_cylinder(leg_radius, leg_height, 32, 32)
    glPopMatrix()

    # second leg
    glPushMatrix()
    glTranslatef(-top_width / 2 + leg_radius,-1+ leg_radius, 0)
    draw_cylinder(leg_radius, leg_height, 32, 32)
    glPopMatrix()

    # third leg
    glPushMatrix()
    glTranslatef(top_width / 2 - leg_radius, -leg_radius, 0)
    draw_cylinder(leg_radius, leg_height, 32, 32)
    glPopMatrix()

    # forth leg
    glPushMatrix()
    glTranslatef(top_width / 2 - leg_radius,-1+ leg_radius, 0)
    draw_cylinder(leg_radius, leg_height, 32, 32)
    glPopMatrix()

    glPopMatrix()

    glPopMatrix()

def draw_cylinder(radius, height, slices, stacks):
    """ Draw a cylinder """
    glPushMatrix()
    glTranslatef(0, height / 2, 0)
    gluCylinder(gluNewQuadric(), radius, radius, height, slices, stacks)
    glPopMatrix()

def myDisplay():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Clear the color buffer and the depth buffer
    glLoadIdentity()
    # Set camera position and orientation
    gluLookAt(camera_distance * sin(camera_angle_y * pi / 180.0) * cos(camera_angle_x * pi / 180.0),
              camera_distance * sin(camera_angle_x * pi / 180.0),
              camera_distance * cos(camera_angle_y * pi / 180.0) * cos(camera_angle_x * pi / 180.0),
              0, 0, 0, 0, 1, 0)

    draw_checkerboard()
    draw_robot()
    draw_table()


    glutSwapBuffers()
    glFlush()

def special_key_pressed(key, x, y):
    global camera_angle_x, camera_angle_y, camera_distance, head_angle
    # Adjust camera angles and distance based on arrow key pressed
    if key == GLUT_KEY_UP:
        camera_angle_x += 5.0
    elif key == GLUT_KEY_DOWN:
        camera_angle_x -= 5.0
    elif key == GLUT_KEY_LEFT:
        if move_flag == 0:
            camera_angle_y -= 5.0
        elif move_flag == 1:
            head_angle -= 5.0
    elif key == GLUT_KEY_RIGHT:
        if move_flag == 0:
            camera_angle_y += 5.0
        elif move_flag == 1:
            head_angle += 5.0



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
    glutSpecialFunc(special_key_pressed)
    glutKeyboardFunc(key_pressed)
    glutReshapeFunc(myReshape)
    glClearColor(1, 1, 1, 1)
    glutMainLoop()


if __name__ == "__main__":
    main()
