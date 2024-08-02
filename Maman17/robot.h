#ifndef ROBOT_H
#define ROBOT_H

#include "obb.h"

#define PI 3.14159265358979323846

class Robot {
public:
    float shoulder_angle, elbow_angle, hand_angle, head_angle, rotation_angle_all;
    float speed, acceleration, max_speed;
    Eigen::Vector3f pos, velocity;

    Robot();
    void draw();
    OBB getOBB() const;

private:
    float lerp(float start, float end, float t) const;
    void drawSphere(float radius) const;
    void drawCube() const;
    void drawPrism() const;
    void drawClaw() const;
    void drawArm() const;
    void drawBody() const;
    void drawHeadFeatures() const;
};

#endif // ROBOT_H