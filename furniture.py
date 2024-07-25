from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


def draw_cylinder(radius, height, slices, stacks):
    """ Draw a cylinder """
    glPushMatrix()
    glTranslatef(0, height / 2, 0)
    quadric = gluNewQuadric()
    gluCylinder(gluNewQuadric(), radius, radius, height, slices, stacks)
    gluDeleteQuadric(quadric)
    glPopMatrix()


def draw_table():
    # Table dimensions
    top_width = 2.5
    top_depth = 1.5
    top_height = 0.15
    leg_radius = 0.05
    leg_height = 1.2

    # place the table
    glPushMatrix()
    glScalef(1.5, 1.2, 1.5)
    glTranslatef(4, -1.2, -0.5)


    # draw the table base
    glPushMatrix()
    glColor3f(0.65, 0.32, 0.17)  # Brown color
    glScalef(top_width, top_height, top_depth)
    glutSolidCube(1)
    glPopMatrix()

    # Draw table legs
    glPushMatrix()
    glTranslatef(0,0, top_height)
    glRotatef(90, 1, 0, 0)

    # first leg
    glPushMatrix()
    glTranslatef(- top_width/2 + leg_radius,-leg_radius,  0)
    draw_cylinder(leg_radius, leg_height, 32, 32)
    glPopMatrix()

    # second leg
    glPushMatrix()
    glTranslatef(-top_width / 2 + leg_radius,-top_depth , 0)
    draw_cylinder(leg_radius, leg_height, 32, 32)
    glPopMatrix()

    # third leg
    glPushMatrix()
    glTranslatef(top_width / 2 - leg_radius, -leg_radius, 0)
    draw_cylinder(leg_radius, leg_height, 32, 32)
    glPopMatrix()

    # forth leg
    glPushMatrix()
    glTranslatef(top_width / 2 - leg_radius,-top_depth, 0)
    draw_cylinder(leg_radius, leg_height, 32, 32)
    glPopMatrix()

    glPopMatrix()

    glPopMatrix()


def draw_tresh_can():
    glPushMatrix()

    specular = [1.0, 1.0, 1.0, 1.0]
    shininess = 128.0

    glMaterialfv(GL_FRONT, GL_SPECULAR, specular)
    glMaterialf(GL_FRONT, GL_SHININESS, shininess)
    glColor3f(0.5, 0.5, 0.5)

    glTranslatef(3, -1.8, -1)
    glScalef(2, 2, 2)
    glRotatef(90, 1, 0, 0)
    draw_cylinder(0.15, 0.4, 32,32)

    glColor3f(0, 0, 0)
    glTranslatef(0, 0.2, 0)
    # Draws a circle
    glPushMatrix()
    quadric = gluNewQuadric()
    gluDisk(gluNewQuadric(), 0, 0.15, 32, 1)
    gluDeleteQuadric(quadric)
    glPopMatrix()

    glPopMatrix()
