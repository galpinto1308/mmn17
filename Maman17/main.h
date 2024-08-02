#ifndef MAIN_H
#define MAIN_H

#include <Eigen/Dense>
#include <unordered_map>
#include "camera.h"
#include "robot.h"
#include "environment.h"
#include "furniture.h"

extern int window_width;
extern int window_height;

extern float camera_angle_x;
extern float camera_angle_y;
extern float camera_distance;

extern float ambient_factor;
extern float lamp_intensity;
extern Eigen::Vector3f lamp_position;
extern Eigen::Vector3f lamp_direction;

extern bool move_flag;
extern bool robot_view;
extern bool lamp_flag;
extern bool lamp_dir_flag;
extern bool lamp_int_flag;

extern std::unordered_map<char, bool> keys;

extern Robot robot;
extern Environment environment;
extern Furniture furniture;

void cleanFlags();
void menu();
void myDisplay();
void myReshape(int width, int height);
void lighting();
float clamp(float value, float min, float max);
void keyPressed(int key, int x, int y);
void updateMove(unsigned char key, int x, int y);
void keyRelease(unsigned char key, int x, int y);
void updateVelocity();
void timer(int value);

#endif // MAIN_H
