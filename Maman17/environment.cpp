#include "environment.h"
#include <GL/freeglut.h>
#include <Eigen/Dense>

Environment::Environment(int rows, int columns, float size, float wall_height)
    : rows(rows), columns(columns), size(size), wall_height(wall_height) {}

void Environment::drawCheckerboard() {
    glPushMatrix();
    glNormal3f(0, 1, 0); 

    glTranslatef(-(rows / 2) - 2, -2.75, -(columns / 2) - 7);

    GLfloat specular[] = {1.0, 1.0, 1.0, 1.0};
    GLfloat shininess = 128.0;

    glMaterialfv(GL_FRONT, GL_SPECULAR, specular);
    glMaterialf(GL_FRONT, GL_SHININESS, shininess);
    glBegin(GL_QUADS);
    for (int row = 0; row < rows; ++row) {
        for (int col = 0; col < columns; ++col) {
            if ((row + col) % 2 == 0) {
                glColor3f(1, 1, 1);
            } else {
                glColor3f(0, 0, 0);
            }

            glVertex3f(col * size, 0,  row * size);
            glVertex3f(col * size, 0, (row + 1) * size);
            glVertex3f((col + 1) * size, 0, (row + 1) * size);
            glVertex3f((col + 1) * size, 0, row * size);
        }
    }
    glEnd();
    glPopMatrix();
}

void Environment::drawWalls() {
    glPushMatrix();
    glTranslatef(-(rows / 2) - 2, -2.75, -(columns / 2) - 7);

    glColor3f(0.6, 0.6, 0.6);
    glBindTexture(GL_TEXTURE_2D, (*texture_ids)["textures/walls.jpg"]);

    // Left wall
    glBegin(GL_QUADS);
    glTexCoord2f(0.0f, 0.0f); glVertex3f(0, 0, 0);
    glTexCoord2f(1.0f, 0.0f); glVertex3f(0, wall_height, 0);
    glTexCoord2f(1.0f, 1.0f); glVertex3f(0, wall_height, columns * size);
    glTexCoord2f(0.0f, 1.0f); glVertex3f(0, 0, columns * size);
    glEnd();

    // Right wall
    glBegin(GL_QUADS);
    glTexCoord2f(0.0f, 0.0f); glVertex3f(rows * size, 0, 0);
    glTexCoord2f(1.0f, 0.0f); glVertex3f(rows * size, wall_height, 0);
    glTexCoord2f(1.0f, 1.0f); glVertex3f(rows * size, wall_height, columns * size);
    glTexCoord2f(0.0f, 1.0f); glVertex3f(rows * size, 0, columns * size);
    glEnd();

    // Front wall
    glBegin(GL_QUADS);
    glTexCoord2f(0.0f, 0.0f); glVertex3f(0, 0, 0);
    glTexCoord2f(1.0f, 0.0f); glVertex3f(0, wall_height, 0);
    glTexCoord2f(1.0f, 1.0f); glVertex3f(rows * size, wall_height, 0);
    glTexCoord2f(0.0f, 1.0f); glVertex3f(rows * size, 0, 0);
    glEnd();

    // Back wall
    glBegin(GL_QUADS);
    glTexCoord2f(0.0f, 0.0f); glVertex3f(0, 0, columns * size);
    glTexCoord2f(1.0f, 0.0f); glVertex3f(0, wall_height, columns * size);
    glTexCoord2f(1.0f, 1.0f); glVertex3f(rows * size, wall_height, columns * size);
    glTexCoord2f(0.0f, 1.0f); glVertex3f(rows * size, 0, columns * size);
    glEnd();

    glBindTexture(GL_TEXTURE_2D, 0);
    glPopMatrix();
}


void Environment::createWallObbs() {
    Eigen::Vector3f center_shift(-(rows / 2) - 2, -2.75, -(columns / 2) - 7);

    Eigen::Vector3f half_size_vertical(0.1, wall_height / 2, columns * size / 2);
    Eigen::Vector3f half_size_horizontal(rows * size / 2, wall_height / 2, 0.1);

    Eigen::Vector3f center;
    Eigen::Matrix3f rotation = Eigen::Matrix3f::Identity();

    // Left wall OBB
    center = center_shift + Eigen::Vector3f(0, wall_height / 2, columns * size / 2);
    wall_obbs.emplace_back(center, half_size_vertical, rotation);

    // Right wall OBB
    center = center_shift + Eigen::Vector3f(rows * size, wall_height / 2, columns * size / 2);
    wall_obbs.emplace_back(center, half_size_vertical, rotation);

    // Front wall OBB
    center = center_shift + Eigen::Vector3f(rows * size / 2, wall_height / 2, 0);
    wall_obbs.emplace_back(center, half_size_horizontal, rotation);

    // Back wall OBB
    center = center_shift + Eigen::Vector3f(rows * size / 2, wall_height / 2, columns * size);
    wall_obbs.emplace_back(center, half_size_horizontal, rotation);
}
