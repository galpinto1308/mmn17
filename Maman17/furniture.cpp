#include "furniture.h"

void Furniture::drawCylinder(float radius, float height, int slices, int stacks) const {
    glPushMatrix();
    glTranslatef(0, height / 2, 0);
    GLUquadric* quadric = gluNewQuadric();
    gluCylinder(quadric, radius, radius, height, slices, stacks);
    gluDeleteQuadric(quadric);
    glPopMatrix();
}

void Furniture::drawTable() const {
    float top_width = 2.5f;
    float top_depth = 1.5f;
    float top_height = 0.15f;
    float leg_radius = 0.05f;
    float leg_height = 1.2f;

    glPushMatrix();
    glScalef(1.5f, 1.2f, 1.5f);
    glTranslatef(4.0f, -1.2f, -0.5f);

    glPushMatrix();
    glColor3f(0.65f, 0.32f, 0.17f);
    glScalef(top_width, top_height, top_depth);
    glutSolidCube(1.0f);
    glPopMatrix();

    glPushMatrix();
    glTranslatef(0.0f, 0.0f, top_height);
    glRotatef(90, 1, 0, 0);

    glPushMatrix();
    glTranslatef(-top_width / 2 + leg_radius, -leg_radius, 0);
    drawCylinder(leg_radius, leg_height, 32, 32);
    glPopMatrix();

    glPushMatrix();
    glTranslatef(-top_width / 2 + leg_radius, -top_depth + leg_radius, 0);
    drawCylinder(leg_radius, leg_height, 32, 32);
    glPopMatrix();

    glPushMatrix();
    glTranslatef(top_width / 2 - leg_radius, -leg_radius, 0);
    drawCylinder(leg_radius, leg_height, 32, 32);
    glPopMatrix();

    glPushMatrix();
    glTranslatef(top_width / 2 - leg_radius, -top_depth + leg_radius, 0);
    drawCylinder(leg_radius, leg_height, 32, 32);
    glPopMatrix();

    glPopMatrix();

    glPopMatrix();
}

void Furniture::drawTrashCan() const {
    glPushMatrix();

    GLfloat ambient[] = {0.1f, 0.1f, 0.1f, 1.0f};
    GLfloat diffuse[] = {0.4f, 0.4f, 0.4f, 1.0f};
    GLfloat specular[] = {1.0f, 1.0f, 1.0f, 1.0f};
    GLfloat shininess = 128.0f;

    glMaterialfv(GL_FRONT, GL_AMBIENT, ambient);
    glMaterialfv(GL_FRONT, GL_DIFFUSE, diffuse);
    glMaterialfv(GL_FRONT, GL_SPECULAR, specular);
    glMaterialf(GL_FRONT, GL_SHININESS, shininess);
    glColor3f(0.5f, 0.5f, 0.5f);

    glTranslatef(3.0f, -1.8f, -1.0f);
    glScalef(2.5f, 2.2f, 2.5f);
    glRotatef(90, 1, 0, 0);
    drawCylinder(0.15f, 0.4f, 32, 32);

    glColor3f(0.0f, 0.0f, 0.0f);
    glTranslatef(0.0f, 0.2f, 0.0f);
    glPushMatrix();
    GLUquadric* quadric = gluNewQuadric();
    gluDisk(quadric, 0.0, 0.15, 32, 1);
    gluDeleteQuadric(quadric);
    glPopMatrix();

    glPopMatrix();
}

OBB Furniture::getTableOBB() const {
    float top_width = 2.5f * 1.5f;
    float top_depth = 1.5f * 1.5f;
    float top_height = 0.15f * 1.2f;
    float leg_radius = 0.05f * 1.5f;
    float leg_height = 1.2f * 1.2f;

    Eigen::Vector3f top_center(4.0f, -1.2f + leg_height + top_height / 2.0f, -0.5f);
    Eigen::Vector3f top_half_sizes(top_width / 2.0f, top_height / 2.0f, top_depth / 2.0f);

    Eigen::Vector3f leg_half_sizes(leg_radius, leg_height / 2.0f, leg_radius);

    Eigen::Matrix3f rotation_matrix = Eigen::Matrix3f::Identity();

    OBB table_top_obb(top_center, top_half_sizes, rotation_matrix);

    std::vector<Eigen::Vector3f> leg_centers = {
        {4.0f - top_width / 2.0f + leg_radius, -1.2f + leg_height / 2.0f, -0.5f - top_depth / 2.0f + leg_radius},
        {4.0f - top_width / 2.0f + leg_radius, -1.2f + leg_height / 2.0f, -0.5f + top_depth / 2.0f - leg_radius},
        {4.0f + top_width / 2.0f - leg_radius, -1.2f + leg_height / 2.0f, -0.5f - top_depth / 2.0f + leg_radius},
        {4.0f + top_width / 2.0f - leg_radius, -1.2f + leg_height / 2.0f, -0.5f + top_depth / 2.0f - leg_radius}
    };

    std::vector<OBB> leg_obbs;
    for (const auto& center : leg_centers) {
        leg_obbs.emplace_back(center, leg_half_sizes, rotation_matrix);
    }

    OBB combined_obb = table_top_obb;
    for (const auto& leg_obb : leg_obbs) {
        combined_obb = combined_obb.combine(leg_obb);
    }

    return combined_obb;
}

OBB Furniture::getTrashCanOBB() const {
    float radius = 0.15f * 2.5f / 100.0f;
    float height = 0.4f * 2.2f;

    Eigen::Vector3f center(3.0f, -1.8f + height / 2.0f, -1.0f);
    Eigen::Vector3f half_sizes(radius, height / 2.0f, radius);

    Eigen::Matrix3f rotation_matrix = Eigen::Matrix3f::Identity();

    return OBB(center, half_sizes, rotation_matrix);
}
