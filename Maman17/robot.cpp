#include "robot.h"
#include <GL/freeglut.h>
#include <Eigen/Dense>

Robot::Robot()
    : shoulder_angle(0), elbow_angle(0), hand_angle(0), head_angle(0),
      rotation_angle_all(0), speed(2.5f), acceleration(0.2f), max_speed(4.0f),
      pos(Eigen::Vector3f::Zero()), velocity(Eigen::Vector3f::Zero()) {}

float Robot::lerp(float start, float end, float t) const {
    return start + t * (end - start);
}

void Robot::drawSphere(float radius) const {
    GLUquadric* quadric = gluNewQuadric();
    gluSphere(quadric, radius, 20, 20);
    gluDeleteQuadric(quadric);
}

void Robot::drawCube() const {
    glutSolidCube(1.0);
}

void Robot::drawPrism() const {
    glBegin(GL_QUADS);
    // Front face
    glVertex3f(-0.5, -0.5,  0.5);
    glVertex3f( 0.5, -0.5,  0.5);
    glVertex3f( 0.5,  0.5,  0.5);
    glVertex3f(-0.5,  0.5,  0.5);
    // Back face
    glVertex3f(-0.5, -0.5, -0.5);
    glVertex3f( 0.5, -0.5, -0.5);
    glVertex3f( 0.5,  0.5, -0.5);
    glVertex3f(-0.5,  0.5, -0.5);
    // Top face
    glVertex3f(-0.5,  0.5, -0.5);
    glVertex3f( 0.5,  0.5, -0.5);
    glVertex3f( 0.5,  0.5,  0.5);
    glVertex3f(-0.5,  0.5,  0.5);
    // Bottom face
    glVertex3f(-0.5, -0.5, -0.5);
    glVertex3f( 0.5, -0.5, -0.5);
    glVertex3f( 0.5, -0.5,  0.5);
    glVertex3f(-0.5, -0.5,  0.5);
    // Right face
    glVertex3f( 0.5, -0.5, -0.5);
    glVertex3f( 0.5,  0.5, -0.5);
    glVertex3f( 0.5,  0.5,  0.5);
    glVertex3f( 0.5, -0.5,  0.5);
    // Left face
    glVertex3f(-0.5, -0.5, -0.5);
    glVertex3f(-0.5,  0.5, -0.5);
    glVertex3f(-0.5,  0.5,  0.5);
    glVertex3f(-0.5, -0.5,  0.5);
    glEnd();
}

void Robot::drawClaw() const {
    glTranslatef(0, -0.65, 0.0);
    glColor3f(0.1f, 0.0f, 0.0f);
    glPushMatrix();
    glScalef(1.3f, 1.0f, 0.6f);
    drawSphere(0.5f);
    glPopMatrix();
    glColor3f(1.0f, 0.0f, 0.0f);

    // Draw the first prism
    glTranslatef(0.0f, -1.5f, 0.0f);
    glPushMatrix();
    glTranslatef(-0.5f, 0.0f, 0.0f);
    glRotatef(-45, 0.0f, 0.0f, 1.0f);
    glScalef(1.0f, 2.0f, 0.5f);
    drawPrism();
    glPopMatrix();

    // Draw the second prism
    glPushMatrix();
    glTranslatef(0.5f, 0.0f, 0.0f);
    glRotatef(45, 0.0f, 0.0f, 1.0f);
    glScalef(1.0f, 2.0f, 0.5f);
    drawPrism();
    glPopMatrix();
}

void Robot::drawArm() const {
    glColor3f(0.1f, 0.2f, 0.1f);

    // Draw the shoulder
    glPushMatrix();
    glRotatef(shoulder_angle, 1.0f, 0.0f, 0.0f);
    glTranslatef(-0.88f, 0, 0.0f);
    glPushMatrix();
    glScalef(0.5f, 0.5f, 0.5f);  // Scale to make a rectangular shape
    drawCube();
    glPopMatrix();

    glTranslatef(0.0f, -0.5f, 0.0f);
    // Draw the elbow
    glPushMatrix();
    glScalef(0.5f, 0.5f, 0.5f);
    drawCube();
    glPopMatrix();

    glRotatef(elbow_angle, 1.0f, 0.0f, 0.0f);
    glScalef(0.5f, 1.0f, 0.5f);
    glTranslatef(0, elbow_angle / 50.0f, elbow_angle / 130.0f);
    glPushMatrix();
    glScalef(0.999f, 1.0f, 1.0f);
    drawCube();
    glPopMatrix();

    // Draw the hand (claw)
    glTranslatef(0, -0.45f, 0);
    glRotatef(hand_angle, 0.0f, 1.0f, 0.0f);
    glPushMatrix();
    glScalef(0.2f, 0.15f, 0.3f);
    drawClaw();
    glPopMatrix();

    glPopMatrix();
}

void Robot::drawBody() const {
    glTranslatef(0.0f, 0.25f, 0.0f);
    glRotatef(90, 1, 0, 0);
    glScalef(1.3f, 1.1f, 1.75f);

    // Create a quadric object
    GLUquadric* quadric = gluNewQuadric();
    gluQuadricNormals(quadric, GLU_SMOOTH);

    // Draw the cylinder
    gluCylinder(quadric, 0.5, 0.5, 1.0, 20, 20);

    // Draw the bottom cap
    glPushMatrix();
    glTranslatef(0.0f, 0.0f, 0.0f);  // move to the bottom
    gluDisk(quadric, 0.0, 0.5, 20, 1);
    glPopMatrix();

    // Draw the top cap
    glPushMatrix();
    glTranslatef(0.0f, 0.0f, 1.0f);  // move to the top
    gluDisk(quadric, 0.0, 0.5, 20, 1);
    glPopMatrix();

    // Delete the quadric object
    gluDeleteQuadric(quadric);
}

void Robot::drawHeadFeatures() const {
    glPushMatrix();
    glRotatef(head_angle, 0, 1, 0);
    glScalef(2.0f, 1.0f, 1.0f);

    // head
    glutSolidCube(0.5f);
    glEnable(GL_BLEND);
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
    glEnable(GL_LINE_SMOOTH);
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST);
    glColor3f(0, 0, 0);
    glLineWidth(1.5f);
    glutWireCube(0.5f);

    // eyes
    glColor3f(0, 0, 0);
    glPushMatrix();
    glTranslatef(-0.1f, 0.12f, 0.26f);
    glutSolidSphere(0.05f, 32, 32);
    glPopMatrix();

    glPushMatrix();
    glTranslatef(0.1f, 0.12f, 0.26f);
    glutSolidSphere(0.05f, 32, 32);
    glPopMatrix();

    // Nose
    glPushMatrix();
    glTranslatef(0, 0, 0.26f);
    glBegin(GL_TRIANGLES);
    glVertex3f(-0.025f, 0, 0);
    glVertex3f(0.025f, 0, 0);
    glVertex3f(0, 0.05f, 0);
    glEnd();
    glPopMatrix();

    // Mouth
    glPushMatrix();
    glScalef(2.0f, 1.0f, 1.0f);
    glBegin(GL_QUADS);
    glVertex3f(-0.075f / 2, -0.1f, 0.26f);
    glVertex3f(0.075f / 2, -0.1f, 0.26f);
    glVertex3f(0.075f / 2, -0.15f, 0.26f);
    glVertex3f(-0.075f / 2, -0.15f, 0.26f);
    glEnd();
    glPopMatrix();
    glPopMatrix();
}

void Robot::draw() {
    glPushMatrix();
    glColor3f(1.0f, 0.0f, 0.0f);  // Red color
    glTranslatef(pos[0], pos[1], pos[2]);
    glRotatef(rotation_angle_all, 0, 1, 0);

    glPushMatrix();
    glTranslatef(0, 0.56f, 0);
    glScalef(1, 1.2f, 1);
    drawHeadFeatures();
    glPopMatrix();

    glColor3f(1.0f, 0.0f, 0.0f);

    // Body (cylinder)
    glPushMatrix();
    drawBody();
    glPopMatrix();

    glPushMatrix();
    drawArm();
    glPopMatrix();

    glPushMatrix();
    glScalef(-1, 1, 1);
    drawArm();
    glPopMatrix();

    // Legs (cubes)
    glPushMatrix();
    glTranslatef(0.3f, -2.0f, 0.0f);
    glScalef(0.5f, 1.0f, 0.5f);  // Scale down and elongate the cube
    drawCube();
    glPopMatrix();

    glPushMatrix();
    glTranslatef(-0.3f, -2.0f, 0.0f);
    glScalef(0.5f, 1.0f, 0.5f);  // Scale down and elongate the cube
    drawCube();
    glPopMatrix();

    glPopMatrix();
}

OBB Robot::getOBB() const {
    Eigen::Vector3f half_sizes(1.38f, 2.5f, 0.875f);  // This encompasses the entire robot

    // Create the rotation matrix for the OBB based on the rotation angle of the robot
    float angle_rad = rotation_angle_all * PI / 180.0f;
    float cos_angle = std::cos(angle_rad);
    float sin_angle = std::sin(angle_rad);
    Eigen::Matrix3f rotation_matrix;
    rotation_matrix << cos_angle, 0, -sin_angle,
                       0,         1, 0,
                       sin_angle, 0, cos_angle;

    return OBB(pos, half_sizes, rotation_matrix);
}

