#include "robot.h"

Robot::Robot()
    : shoulder_angle(0), elbow_angle(0), hand_angle(0), head_angle(0),
    rotation_angle_all(0), speed(2.5f), acceleration(0.2f), max_speed(4.0f),
    pos(Eigen::Vector3f::Zero()), velocity(Eigen::Vector3f::Zero()) {}

float Robot::lerp(float start, float end, float t) const {
    return start + t * (end - start);
}

void Robot::setShinyMaterial() const {
    GLfloat mat_specular[] = { 1.0, 1.0, 1.0, 1.0 };
    GLfloat mat_shininess[] = { 50.0 };
    GLfloat mat_ambient[] = { 0.25, 0.25, 0.25, 1.0 };
    GLfloat mat_diffuse[] = { 0.4, 0.4, 0.4, 1.0 };

    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular);
    glMaterialfv(GL_FRONT, GL_SHININESS, mat_shininess);
    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient);
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse);
}

void Robot::drawCubeWithTexture() const
{
    glBegin(GL_QUADS);
    // Front face
    glTexCoord2f(0.0f, 0.0f); glVertex3f(-0.25f, -0.25f, 0.25f);
    glTexCoord2f(1.0f, 0.0f); glVertex3f(0.25f, -0.25f, 0.25f);
    glTexCoord2f(1.0f, 1.0f); glVertex3f(0.25f, 0.25f, 0.25f);
    glTexCoord2f(0.0f, 1.0f); glVertex3f(-0.25f, 0.25f, 0.25f);
    // Back face
    glTexCoord2f(0.0f, 0.0f); glVertex3f(-0.25f, -0.25f, -0.25f);
    glTexCoord2f(1.0f, 0.0f); glVertex3f(0.25f, -0.25f, -0.25f);
    glTexCoord2f(1.0f, 1.0f); glVertex3f(0.25f, 0.25f, -0.25f);
    glTexCoord2f(0.0f, 1.0f); glVertex3f(-0.25f, 0.25f, -0.25f);
    // Top face
    glTexCoord2f(0.0f, 0.0f); glVertex3f(-0.25f, 0.25f, -0.25f);
    glTexCoord2f(1.0f, 0.0f); glVertex3f(0.25f, 0.25f, -0.25f);
    glTexCoord2f(1.0f, 1.0f); glVertex3f(0.25f, 0.25f, 0.25f);
    glTexCoord2f(0.0f, 1.0f); glVertex3f(-0.25f, 0.25f, 0.25f);
    // Bottom face
    glTexCoord2f(0.0f, 0.0f); glVertex3f(-0.25f, -0.25f, -0.25f);
    glTexCoord2f(1.0f, 0.0f); glVertex3f(0.25f, -0.25f, -0.25f);
    glTexCoord2f(1.0f, 1.0f); glVertex3f(0.25f, -0.25f, 0.25f);
    glTexCoord2f(0.0f, 1.0f); glVertex3f(-0.25f, -0.25f, 0.25f);
    // Right face
    glTexCoord2f(0.0f, 0.0f); glVertex3f(0.25f, -0.25f, -0.25f);
    glTexCoord2f(1.0f, 0.0f); glVertex3f(0.25f, 0.25f, -0.25f);
    glTexCoord2f(1.0f, 1.0f); glVertex3f(0.25f, 0.25f, 0.25f);
    glTexCoord2f(0.0f, 1.0f); glVertex3f(0.25f, -0.25f, 0.25f);
    // Left face
    glTexCoord2f(0.0f, 0.0f); glVertex3f(-0.25f, -0.25f, -0.25f);
    glTexCoord2f(1.0f, 0.0f); glVertex3f(-0.25f, -0.25f, 0.25f);
    glTexCoord2f(1.0f, 1.0f); glVertex3f(-0.25f, 0.25f, 0.25f);
    glTexCoord2f(0.0f, 1.0f); glVertex3f(-0.25f, 0.25f, -0.25f);
    glEnd();
}

void Robot::drawPrism() const {
    glBegin(GL_QUADS);
    // Front face
    glTexCoord2f(0.0f, 0.0f); glVertex3f(-0.5f, -0.5f, 0.5f);
    glTexCoord2f(1.0f, 0.0f); glVertex3f(0.5f, -0.5f, 0.5f);
    glTexCoord2f(1.0f, 1.0f); glVertex3f(0.5f, 0.5f, 0.5f);
    glTexCoord2f(0.0f, 1.0f); glVertex3f(-0.5f, 0.5f, 0.5f);
    // Back face
    glTexCoord2f(0.0f, 0.0f); glVertex3f(-0.5f, -0.5f, -0.5f);
    glTexCoord2f(1.0f, 0.0f); glVertex3f(0.5f, -0.5f, -0.5f);
    glTexCoord2f(1.0f, 1.0f); glVertex3f(0.5f, 0.5f, -0.5f);
    glTexCoord2f(0.0f, 1.0f); glVertex3f(-0.5f, 0.5f, -0.5f);
    // Top face
    glTexCoord2f(0.0f, 0.0f); glVertex3f(-0.5f, 0.5f, -0.5f);
    glTexCoord2f(1.0f, 0.0f); glVertex3f(0.5f, 0.5f, -0.5f);
    glTexCoord2f(1.0f, 1.0f); glVertex3f(0.5f, 0.5f, 0.5f);
    glTexCoord2f(0.0f, 1.0f); glVertex3f(-0.5f, 0.5f, 0.5f);
    // Bottom face
    glTexCoord2f(0.0f, 0.0f); glVertex3f(-0.5f, -0.5f, -0.5f);
    glTexCoord2f(1.0f, 0.0f); glVertex3f(0.5f, -0.5f, -0.5f);
    glTexCoord2f(1.0f, 1.0f); glVertex3f(0.5f, -0.5f, 0.5f);
    glTexCoord2f(0.0f, 1.0f); glVertex3f(-0.5f, -0.5f, 0.5f);
    // Right face
    glTexCoord2f(0.0f, 0.0f); glVertex3f(0.5f, -0.5f, -0.5f);
    glTexCoord2f(1.0f, 0.0f); glVertex3f(0.5f, 0.5f, -0.5f);
    glTexCoord2f(1.0f, 1.0f); glVertex3f(0.5f, 0.5f, 0.5f);
    glTexCoord2f(0.0f, 1.0f); glVertex3f(0.5f, -0.5f, 0.5f);
    // Left face
    glTexCoord2f(0.0f, 0.0f); glVertex3f(-0.5f, -0.5f, -0.5f);
    glTexCoord2f(1.0f, 0.0f); glVertex3f(-0.5f, -0.5f, 0.5f);
    glTexCoord2f(1.0f, 1.0f); glVertex3f(-0.5f, 0.5f, 0.5f);
    glTexCoord2f(0.0f, 1.0f); glVertex3f(-0.5f, 0.5f, -0.5f);
    glEnd();
}

void Robot::drawTexturedCylinder(GLfloat radius, GLfloat height, GLint slices, GLint stacks) const {
    GLfloat angleStep = 2.0f * PI / slices;
    GLfloat stackHeight = height / stacks;

    for (GLint i = 0; i < stacks; ++i) {
        GLfloat z0 = i * stackHeight;
        GLfloat z1 = (i + 1) * stackHeight;

        glBegin(GL_QUAD_STRIP);
        for (GLint j = 0; j <= slices; ++j) {
            GLfloat angle = j * angleStep;
            GLfloat x = radius * cos(angle);
            GLfloat y = radius * sin(angle);
            glTexCoord2f((GLfloat)j / slices, (GLfloat)i / stacks);
            glVertex3f(x, y, z0);
            glTexCoord2f((GLfloat)j / slices, (GLfloat)(i + 1) / stacks);
            glVertex3f(x, y, z1);
        }
        glEnd();
    }
}

void Robot::drawTexturedDisk(GLfloat innerRadius, GLfloat outerRadius, GLint slices) const {
    GLfloat angleStep = 2.0f * PI / slices;

    glBegin(GL_TRIANGLE_STRIP);
    for (GLint i = 0; i <= slices; ++i) {
        GLfloat angle = i * angleStep;
        GLfloat x = cos(angle);
        GLfloat y = sin(angle);

        glTexCoord2f(0.5f + 0.5f * x, 0.5f + 0.5f * y);
        glVertex2f(innerRadius * x, innerRadius * y);
        glTexCoord2f(0.5f + 0.5f * x, 0.5f + 0.5f * y);
        glVertex2f(outerRadius * x, outerRadius * y);
    }
    glEnd();
}

void Robot::drawClaw() const 
{
    glBindTexture(GL_TEXTURE_2D, 0);

    // Set the material to non-shiny
    GLfloat no_specular[] = { 0.0f, 0.0f, 0.0f, 1.0f };
    glMaterialfv(GL_FRONT, GL_SPECULAR, no_specular);
    glMateriali(GL_FRONT, GL_SHININESS, 0);

    glColor3f(0.0f, 0.0f, 0.0f);
    glTranslatef(0, -0.65f, 0.0f);
    glPushMatrix();
    glScalef(1.3f, 1.0f, 0.6f);
    auto quadric = gluNewQuadric();
    gluSphere(quadric, 0.5, 20, 20);
    glPopMatrix();

    glColor3f(1.0f, 0.0f, 0.0f);
    // Draw the first prism
    glTranslatef(0.0f, -1.5f, 0.0f);
    glPushMatrix();
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
    glPopMatrix();

    glColor3f(1.0f, 1.0f, 1.0f);
    gluDeleteQuadric(quadric);
}

void Robot::drawArm() const {
    // Bind the texture for the arm
    glBindTexture(GL_TEXTURE_2D, (*texture_ids)["textures/robot_texture.jpg"]);

    // Draw the shoulder
    glPushMatrix();
    setShinyMaterial();
    glRotatef(shoulder_angle, 1.0f, 0.0f, 0.0f);
    glTranslatef(-0.88f, 0, 0.0f);
    glPushMatrix();
    glScalef(0.5f, 0.5f, 0.5f);  // Scale to make a rectangular shape
    drawPrism();
    glPopMatrix();

    glTranslatef(0.0f, -0.5f, 0.0f);
    // Draw the elbow
    glPushMatrix();
    setShinyMaterial();
    glScalef(0.5f, 0.5f, 0.5f);
    drawPrism();
    glPopMatrix();

    glRotatef(elbow_angle, 1.0f, 0.0f, 0.0f);
    glScalef(0.5f, 1.0f, 0.5f);
    glTranslatef(0, elbow_angle / 50.0f, elbow_angle / 130.0f);
    glPushMatrix();
    setShinyMaterial();
    glScalef(1.0f, 1.0f, 1.0f);
    drawPrism();
    glPopMatrix();

    glColor3f(1.0, 0, 0);
    glTranslatef(0, -0.45f, 0);
    glRotatef(hand_angle, 0.0f, 1.0f, 0.0f);

    glPushMatrix();
    glScalef(0.2f, 0.15f, 0.3f);
    drawClaw();
    glPopMatrix();

    glPopMatrix();
}

void Robot::drawBody() const 
{
    glColor3f(1.0f, 1.0f, 1.0f);
    setShinyMaterial();

    // Bind the texture for the body
    glBindTexture(GL_TEXTURE_2D, (*texture_ids)["textures/robot_texture.jpg"]);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);

    glTranslatef(0.0f, 0.25f, 0.0f);
    glRotatef(90, 1, 0, 0);
    glScalef(1.3f, 1.1f, 1.75f);

    // Draw the cylinder
    drawTexturedCylinder(0.5, 1.0, 20, 20);

    // Draw the bottom cap
    glPushMatrix();
    glTranslatef(0.0f, 0.0f, 0.0f);  // move to the bottom
    drawTexturedDisk(0.0, 0.5, 20);
    glPopMatrix();

    // Draw the top cap
    glPushMatrix();
    glTranslatef(0.0f, 0.0f, 1.0f);  // move to the top
    drawTexturedDisk(0.0, 0.5, 20);
    glPopMatrix();
}

void Robot::drawHeadFeatures() const {
    glPushMatrix();
    glRotatef(head_angle, 0, 1, 0);
    glScalef(2.0f, 1.0f, 1.0f);

    // head
    glBindTexture(GL_TEXTURE_2D, (*texture_ids)["textures/robot_texture.jpg"]);
    drawCubeWithTexture();
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
    glColor3f(1.0, 1.0, 1.0);

    glTranslatef(pos[0], pos[1], pos[2]);
    glRotatef(rotation_angle_all, 0, 1, 0);

    // Draw head
    glPushMatrix();
    setShinyMaterial();
    glTranslatef(0, 0.56f, 0);
    glScalef(1, 1.2f, 1);
    drawHeadFeatures();
    glPopMatrix();

    glColor3f(1.0, 1.0, 1.0);

    // Draw body (cylinder)
    glPushMatrix();
    setShinyMaterial();
    drawBody();
    glPopMatrix();

    // Draw arms
    glPushMatrix();
    drawArm();
    glPopMatrix();

    glPushMatrix();
    glScalef(-1, 1, 1);
    drawArm();
    glPopMatrix();

    // Draw legs (cubes)
    glBindTexture(GL_TEXTURE_2D, (*texture_ids)["textures/robot_texture.jpg"]);

    glPushMatrix();
    setShinyMaterial();
    glTranslatef(0.3f, -2.0f, 0.0f);
    glScalef(0.5f, 1.0f, 0.5f);  // Scale down and elongate the cube
    drawPrism();
    glPopMatrix();

    glPushMatrix();
    setShinyMaterial();
    glTranslatef(-0.3f, -2.0f, 0.0f);
    glScalef(0.5f, 1.0f, 0.5f);  // Scale down and elongate the cube
    drawPrism();
    glPopMatrix();

    glPopMatrix();
    glBindTexture(GL_TEXTURE_2D, 0);
}

OBB Robot::getOBB() const {
    Eigen::Vector3f half_sizes(1.38f, 2.5f, 0.875f);  // This encompasses the entire robot

    // Create the rotation matrix for the OBB based on the rotation angle of the robot
    float angle_rad = rotation_angle_all * PI / 180.0f;
    float cos_angle = std::cos(angle_rad);
    float sin_angle = std::sin(angle_rad);
    Eigen::Matrix3f rotation_matrix;
    rotation_matrix << cos_angle, 0, -sin_angle,
        0, 1, 0,
        sin_angle, 0, cos_angle;

    return OBB(pos, half_sizes, rotation_matrix);
}
