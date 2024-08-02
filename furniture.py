import utils
from obb import OBB
from utils import *

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


    glColor3f(1.0, 1.0, 1.0)  # Use white to maintain the texture's color
    glBindTexture(GL_TEXTURE_2D, utils.texture_ids["textures/wood.png"])
    # draw table top
    glPushMatrix()
    glScalef(top_width, top_height, top_depth)
    draw_cube(1.0)
    glPopMatrix()

    # Draw table legs
    glPushMatrix()
    glTranslatef(0,0, top_height)
    glRotatef(90, 1, 0, 0)
    glTranslatef(0, leg_height / 2, 0)

    # first leg
    glPushMatrix()
    glTranslatef(- top_width/2 + leg_radius,-leg_radius,  0)
    draw_cylinder(leg_radius, leg_height, 32, 32)
    glPopMatrix()

    # second leg
    glPushMatrix()
    glTranslatef(-top_width / 2 + leg_radius,-top_depth + leg_radius, 0)
    draw_cylinder(leg_radius, leg_height, 32, 32)
    glPopMatrix()

    # third leg
    glPushMatrix()
    glTranslatef(top_width / 2 - leg_radius, -leg_radius, 0)
    draw_cylinder(leg_radius, leg_height, 32, 32)
    glPopMatrix()

    # forth leg
    glPushMatrix()
    glTranslatef(top_width / 2 - leg_radius,-top_depth + leg_radius, 0)
    draw_cylinder(leg_radius, leg_height, 32, 32)
    glPopMatrix()

    glPopMatrix()

    glPopMatrix()
    glBindTexture(GL_TEXTURE_2D, 0)

def draw_tresh_can():
    glPushMatrix()

    ambient = [0.1, 0.1, 0.1, 1.0]
    diffuse = [0.4, 0.4, 0.4, 1.0]
    specular = [1, 1, 1, 1.0]
    shininess = 128.0

    glMaterialfv(GL_FRONT, GL_AMBIENT, ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specular)
    glMaterialf(GL_FRONT, GL_SHININESS, shininess)
    glColor3f(0.5, 0.5, 0.5)

    glTranslatef(3, -1.8, -1)

    glScalef(2.5, 2.4, 2.5)
    glRotatef(90, 1, 0, 0)

    glColor3f(1.0, 1.0, 1.0)  # Use white to maintain the texture's color
    glBindTexture(GL_TEXTURE_2D, utils.texture_ids["textures/metal.jpg"])
    draw_cylinder(0.15, 0.4, 32,32)
    glBindTexture(GL_TEXTURE_2D, 0)
    glColor3f(0, 0, 0)

    # Draws a circle
    glPushMatrix()
    gluDisk(gluNewQuadric(), 0, 0.15, 32, 1)
    glPopMatrix()

    glPopMatrix()


def draw_table_obb():
    # Table dimensions
    top_width = 2.5 * 1.5
    top_depth = 1.5 * 1.5
    top_height = 0.15 * 1.2
    leg_radius = 0.05 * 1.5
    leg_height = 1.2 * 1.2

    # Calculate the center and half-sizes for the table top
    top_center = [4, -1.2 + leg_height + top_height / 2, -0.5]
    top_half_sizes = [top_width / 2, top_height / 2, top_depth / 2]

    # Calculate the half-sizes for the legs
    leg_half_sizes = [leg_radius, leg_height / 2, leg_radius]
    
    # Rotation matrix for the table (no rotation)
    rotation_matrix = np.eye(3)

    # Create OBB for the table top
    table_top_obb = OBB(top_center, top_half_sizes, rotation_matrix)

    # Calculate the centers for the legs
    leg_centers = [
        [4 - top_width / 2 + leg_radius, -1.2 + leg_height / 2, -0.5 - top_depth / 2 + leg_radius],
        [4 - top_width / 2 + leg_radius, -1.2 + leg_height / 2, -0.5 + top_depth / 2 - leg_radius],
        [4 + top_width / 2 - leg_radius, -1.2 + leg_height / 2, -0.5 - top_depth / 2 + leg_radius],
        [4 + top_width / 2 - leg_radius, -1.2 + leg_height / 2, -0.5 + top_depth / 2 - leg_radius],
    ]
    
    # Create OBBs for the legs
    leg_obbs = [OBB(center, leg_half_sizes, rotation_matrix) for center in leg_centers]

    # Combine the OBBs into one
    combined_obb = table_top_obb
    for leg_obb in leg_obbs:
        combined_obb = combined_obb.combine(leg_obb)
    
    return combined_obb

def draw_trash_can_obb():
    # Scaled dimensions of the trash can
    radius = 0.01  # Scaled radius
    height = 0.4 * 2.2  # Scaled height

    # Calculate the center of the OBB
    center = [3, -1.8 + height / 2, -1]

    # Since the trash can is a cylinder, its OBB should reflect that it is taller than it is wide
    half_sizes = [radius, height / 2, radius]

    # No rotation applied to the trash can, so the rotation matrix is the identity matrix
    rotation_matrix = np.eye(3)

    return OBB(center, half_sizes, rotation_matrix)
