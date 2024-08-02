import utils
from obb import OBB
from utils import *
global head_angle, hand_angle, elbow_angle, shoulder_angle, rotation_angle_all
global velocity, acceleration, max_speed, pos, speed

shoulder_angle = 0
elbow_angle = 0
hand_angle = 0
head_angle = 0

pos = [0.0, 0.0, 0.0]
velocity = [0.0, 0.0, 0.0]
speed = 2.5
acceleration = 0.2  # Acceleration for smooth start
max_speed = 4.0  # Maximum speed
rotation_angle_all = 0.0

def lerp(start, end, t):
    return start + t * (end - start)


def draw_claw():
    glTranslatef(0, -0.65, 0.0)
    glColor3f(1, 1, 1)
    glPushMatrix()
    glScalef(1.3, 1, 0.6)
    draw_sphere(0.5)
    glPopMatrix()
    glColor3f(1, 0, 0)

    # Draw the first prism
    glTranslatef(0.0, -1.5, 0.0)
    glPushMatrix()
    glTranslatef(-0.5, 0.0, 0.0)
    glRotatef(-45, 0.0, 0.0, 1.0)
    glScalef(1.0, 2.0, 0.5)
    draw_cube(1.0)
    glPopMatrix()

    # Draw the second prism
    glPushMatrix()
    glTranslatef(0.5, 0.0, 0.0)
    glRotatef(45, 0.0, 0.0, 1.0)
    glScalef(1.0, 2.0, 0.5)
    draw_cube(1.0)
    glPopMatrix()


def draw_arm():
    global shoulder_angle, elbow_angle, hand_angle
    # Draw the shoulder
    glPushMatrix()
    glRotatef(shoulder_angle, 1.0, 0.0, 0.0)
    glTranslatef(-0.88, 0, 0.0)
    glPushMatrix()
    glScalef(0.5, 0.5, 0.5)  # Scale to make a rectangular shape
    draw_cube(1.0)
    glPopMatrix()

    glTranslatef(0.0, -0.5, 0.0)
    # Draw the elbow
    glPushMatrix()
    glScalef(0.5, 0.5, 0.5)
    draw_cube(1.0)
    glPopMatrix()

    glRotatef(elbow_angle, 1.0, 0.0, 0.0)
    glScalef(0.5, 1, 0.5)
    glTranslatef(0, elbow_angle / 50, elbow_angle / 130)
    glPushMatrix()
    glScalef(0.999, 1, 1)
    draw_cube(1.0)
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
    glPushMatrix()
    glTranslatef(0.0, -0.62, 0.0)  # Adjust the translation to position correctly relative to the robot
    glRotatef(90, 1, 0, 0)
    # Scale the cube to be slimmer and fit as the robot's body
    glScalef(1.25, 0.6, 1.75)
    draw_cube(1.0)
    glPopMatrix()

def draw_head_features():
    glPushMatrix()

    # Rotate and scale
    glRotatef(head_angle, 0, 1, 0)
    glScalef(2.0, 1.0, 1.0)
    # head
    draw_cube(0.5)

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
    global pos, rotation_angle_all
    glPushMatrix()
    glColor3f(1.0, 1.0, 1.0)  # Set color to white to apply the texture colors
    glBindTexture(GL_TEXTURE_2D, utils.texture_ids["textures/robot_texture.jpg"])
    glTranslatef(pos[0], pos[1], pos[2])
    glRotatef(rotation_angle_all, 0, 1, 0)
    # Head
    glPushMatrix()
    glTranslatef(0, 0.56, 0)
    glScalef(1, 1.2, 1)
    draw_head_features()
    glPopMatrix()

    # Body
    glColor3f(1.0, 1.0, 1.0)
    glPushMatrix()
    draw_body()
    glPopMatrix()

    # Arms
    glPushMatrix()
    draw_arm()
    glPopMatrix()

    glColor3f(1.0, 1.0, 1.0)
    glPushMatrix()
    glScalef(-1, 1, 1)
    draw_arm()
    glPopMatrix()


    # Legs (cubes)
    glColor3f(1.0, 1.0, 1.0)
    glPushMatrix()
    glTranslatef(0.3, -2.0, 0.0)
    glScalef(0.5, 1.0, 0.5)  # Scale down and elongate the cube
    draw_cube(1.0)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-0.3, -2.0, 0.0)
    glScalef(0.5, 1.0, 0.5)  # Scale down and elongate the cube
    draw_cube(1.0)
    glPopMatrix()
    
    glPopMatrix()
    glBindTexture(GL_TEXTURE_2D, 0)
def draw_robot_obb():
    global pos, rotation_angle_all

    # Define the half-sizes for the OBB (half the dimensions of the bounding box)
    half_sizes = np.array([1.38, 2.5, 0.875])  # This encompasses the entire robot

    # Create the rotation matrix for the OBB based on the rotation angle of the robot
    angle_rad = np.radians(rotation_angle_all)
    cos_angle = np.cos(angle_rad)
    sin_angle = np.sin(angle_rad)
    rotation_matrix = np.array([
        [cos_angle, 0, -sin_angle],
        [0, 1, 0],
        [sin_angle, 0, cos_angle]
    ])

    # Create the OBB
    robot_obb = OBB(pos, half_sizes, rotation_matrix)

    return robot_obb
