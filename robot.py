from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

global head_angle, hand_angle, elbow_angle, shoulder_angle

shoulder_angle = 0
elbow_angle = 0
hand_angle = 0
head_angle = 0

def draw_sphere(radius):
    quadric = gluNewQuadric()
    gluSphere(quadric, radius, 20, 20)
    gluDeleteQuadric(quadric)

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
    global shoulder_angle, elbow_angle, hand_angle
    glColor3f(0.1, 0.2, 0.1)

    # Draw the shoulder
    glPushMatrix()
    glRotatef(shoulder_angle, 1.0, 0.0, 0.0)
    glTranslatef(-0.88, 0, 0.0)
    glPushMatrix()
    glScalef(0.5, 0.5, 0.5)  # Scale to make a rectangular shape
    draw_cube()
    glPopMatrix()

    glTranslatef(0.0, -0.5, 0.0)
    # Draw the elbow
    glPushMatrix()
    glScalef(0.5, 0.5, 0.5)
    draw_cube()
    glPopMatrix()

    glRotatef(elbow_angle, 1.0, 0.0, 0.0)
    glScalef(0.5, 1, 0.5)
    glTranslatef(0, elbow_angle / 50, elbow_angle / 130)
    glPushMatrix()
    glScalef(0.999, 1, 1)
    draw_cube()
    glPopMatrix()

    # Draw the hand (claw)
    glTranslatef(0, -0.45, 0)
    glRotatef(hand_angle, 0.0, 1.0, 0.0)
    glPushMatrix()
    glScalef(0.2, 0.15, 0.3)
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
    glPushMatrix()
    glRotate(head_angle,0,1,0)
    glScalef(2.0, 1.0, 1.0)

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
    glPopMatrix()


def draw_robot():
    glPushMatrix()
    glColor3f(1.0, 0.0, 0.0)  # Red color

    glPushMatrix()
    glTranslatef(0, 0.56, 0)
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
