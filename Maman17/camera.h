#ifndef CAMERA_H
#define CAMERA_H

#include <Eigen/Dense>
#include "obb.h"
#define PI 3.14159265358979323846

class Camera
{
public:
    Eigen::Vector3f position;
    float distance;
    float angle_x;
    float angle_y;
    float size; // Size of the bounding box
    Eigen::Vector3f last_movement;

    Camera(const Eigen::Vector3f& pos, float dist, float size);

    void move(float dx, float dy, float dz);
    void rotate(float ax, float ay);
};

#endif // CAMERA_H
