#ifndef MAIN_H
#define MAIN_H

#include <GL/freeglut.h>
#include <Eigen/Dense>
#include <unordered_map>
#include "robot.h"
#include "environment.h"
#include "furniture.h"

// Window dimensions
extern int window_width;
extern int window_height;

// Camera rotation
extern float camera_angle_x;
extern float camera_angle_y;
extern float camera_distance;

// Lighting variables
extern float ambient_factor;
extern float lamp_intensity;
extern Eigen::Vector3f lamp_position;
extern Eigen::Vector3f lamp_direction;

// Scene flags
extern bool move_flag;
extern bool robot_view;
extern bool lamp_flag;
extern bool lamp_dir_flag;
extern bool lamp_int_flag;

// State to keep track of which keys are pressed
extern std::unordered_map<char, bool> keys;

// Robot, Environment, and Furniture objects
extern Robot robot;
extern Environment environment;
extern Furniture furniture;

// Function declarations
void cleanFlags();
void menu();
void myDisplay();
void myReshape(int width, int height);
void lighting();
void keyPressed(int key, int x, int y);
void updateMove(unsigned char key, int x, int y);
void keyRelease(unsigned char key, int x, int y);
void updateVelocity();
void timer(int value);

#endif // MAIN_H
