#include "camera.h"
#define ENLARGE 4.0f

Camera::Camera(const Eigen::Vector3f& pos, float dist, float size)
    : position(pos), distance(dist), angle_x(30.0f), angle_y(180.0f), size(size), last_movement(0.0f, 0.0f, 0.0f) 
{
    
}

void Camera::move(float dx, float dy, float dz) {
    last_movement = Eigen::Vector3f(dx, dy, dz);
    position += last_movement;
}

void Camera::rotate(float ax, float ay) {
    angle_x += ax;
    angle_y += ay;
}

