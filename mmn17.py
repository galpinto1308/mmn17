from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import sys
import time

import robot
from robot import *
from environment import *
from furniture import *

window_width = 1280
window_height = 860

# Global variables for camera rotation
camera_angle_x = 0.0
camera_angle_y = 0.0
camera_distance = 7.0

ambient_factor = 0.9
move_flag = -1
robot_view = 0

# State to keep track of which keys are pressed
keys = {"a": False, "d": False, "w": False, "s": False}

def myDisplay():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Clear the color buffer and the depth buffer
    glLoadIdentity()
    # Set camera position and orientation
    if robot_view:
        target_offset = [0, 0, 5]  # init point of looking (outside of screen)
        eye_offset = [0, 0.68, 0.25]  # the offset of the robot eyes from its center
        # rotate eyes and target positions around y-axis if needed
        rotation_angle_rad = math.radians(robot.rotation_angle_all + robot.head_angle)

        eye_x = eye_offset[0] * math.cos(rotation_angle_rad) + eye_offset[2] * math.sin(rotation_angle_rad)
        eye_z = eye_offset[2] * math.cos(rotation_angle_rad) - eye_offset[0] * math.sin(rotation_angle_rad)
        eye_position = [robot.pos[0] + eye_x, robot.pos[1] + eye_offset[1], robot.pos[2] + eye_z]

        target_x = target_offset[0] * math.cos(rotation_angle_rad) + target_offset[2] * math.sin(rotation_angle_rad)
        target_z = target_offset[2] * math.cos(rotation_angle_rad) - target_offset[0] * math.sin(rotation_angle_rad)
        target_position = [robot.pos[0] + target_x, robot.pos[1], robot.pos[2] + target_z]

        gluLookAt(eye_position[0], eye_position[1], eye_position[2],
                  target_position[0], target_position[1], target_position[2], 0, 1, 0)
    else:
        gluLookAt(robot.pos[0] + camera_distance * math.sin(camera_angle_y * math.pi / 180.0) * math.cos(
            camera_angle_x * math.pi / 180.0),
                  robot.pos[1] + camera_distance * math.sin(camera_angle_x * math.pi / 180.0),
                  robot.pos[2] + camera_distance * math.cos(camera_angle_y * math.pi / 180.0) * math.cos(
                      camera_angle_x * math.pi / 180.0),
                  robot.pos[0], robot.pos[1], robot.pos[2], 0, 1, 0)
    lighting()
    draw_checkerboard()
    draw_walls()
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
def key_pressed(key, x, y):
    global camera_angle_x, camera_angle_y, camera_distance, ambient_factor

    # If the key is not a number it will return an exception.
    # We want to ignore the exception
    
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

def update_move(key, x, y):
    global move_flag, robot_view
    
    try:
        move_flag = int(key)
    except:
        move_flag = move_flag

    if key == b'a':
        keys["a"] = True
    elif key == b'd':
        keys["d"] = True
    elif key == b'w':
        keys["w"] = True
    elif key == b's':
        keys["s"] = True
    elif key == b'r':
        robot_view = True
    elif move_flag == 0:
        robot_view = False
    update_velocity()
    

def key_release(key, x, y):
    if key == b'a':
        keys["a"] = False
    elif key == b'd':
        keys["d"] = False
    elif key == b'w':
        keys["w"] = False
    elif key == b's':
        keys["s"] = False
    
    robot.look_direction = 0
    update_velocity()

def update_velocity():
    global keys
    
    robot.velocity[0] = (-robot.speed if keys["a"] else 0) + (robot.speed if keys["d"] else 0)
    robot.velocity[2] = (robot.speed if keys["w"] else 0) + (-robot.speed if keys["s"] else 0)

def timer(value):
    current_time = time.time()
    dt = current_time - timer.last_time
    timer.last_time = current_time
    
    robot_bb = draw_robot_obb()
    table_bb = draw_table_obb()
    trash_can_bb = draw_trash_can_obb()
    wall_obbs = draw_wall_obbs()
    
    # Predict new position
    new_pos = [
        robot.pos[0] + robot.velocity[0] * dt,
        robot.pos[1],
        robot.pos[2] + robot.velocity[2] * dt
    ]

    # Predict new orientation
    if velocity[0] != 0 or velocity[2] != 0:
        new_rotation_angle_all = math.degrees(math.atan2(velocity[0], velocity[2]))
    else:
        new_rotation_angle_all = robot.rotation_angle_all

    # Create the OBB for the predicted new position and orientation
    angle_rad = np.radians(new_rotation_angle_all)
    cos_angle = np.cos(angle_rad)
    sin_angle = np.sin(angle_rad)
    rotation_matrix = np.array([
        [cos_angle, 0, -sin_angle],
        [0, 1, 0],
        [sin_angle, 0, cos_angle]
    ])

    new_robot_bb = OBB(new_pos, robot_bb.half_sizes, rotation_matrix)

     # Check for collisions with table, trash can, and walls
    if (not new_robot_bb.intersects(table_bb) and
        not new_robot_bb.intersects(trash_can_bb) and
        not any(new_robot_bb.intersects(wall) for wall in wall_obbs)):
        robot.pos[0] = new_pos[0]
        robot.pos[2] = new_pos[2]

        if robot.velocity[0] != 0 or robot.velocity[2] != 0:
            robot.rotation_angle_all = math.degrees(math.atan2(velocity[0], velocity[2]))
    
    glutPostRedisplay()
    glutTimerFunc(16, timer, 0) # 16 ms for ~60 FPS

# main to initialize the window size and start the main loop of the graphic
def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH | GLUT_MULTISAMPLE)
    glutInitWindowSize(window_width, window_height)
    glutInitWindowPosition(0, 0)
    glutCreateWindow("MMN 17")
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glShadeModel(GL_SMOOTH)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
    
    # Enable general antialiasing
    glEnable(GL_LINE_SMOOTH)
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
    glEnable(GL_POLYGON_SMOOTH)
    glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)
    
    glutDisplayFunc(myDisplay)
    glutSpecialFunc(key_pressed)
    glutKeyboardFunc(update_move)
    glutKeyboardUpFunc(key_release)
    glutReshapeFunc(myReshape)
    timer.last_time = time.time()
    glutTimerFunc(16, timer, 0)  # 16 ms for ~60 FPS
    glutMainLoop()


if __name__ == "__main__":
    main()
