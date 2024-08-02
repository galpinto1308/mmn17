#include "furniture.h"

void Furniture::drawTexturedCube(float width, float height, float depth) const {
    glBegin(GL_QUADS);
    // Front face
    glTexCoord2f(0.0f, 0.0f); glVertex3f(-width / 2, -height / 2, depth / 2);
    glTexCoord2f(1.0f, 0.0f); glVertex3f(width / 2, -height / 2, depth / 2);
    glTexCoord2f(1.0f, 1.0f); glVertex3f(width / 2, height / 2, depth / 2);
    glTexCoord2f(0.0f, 1.0f); glVertex3f(-width / 2, height / 2, depth / 2);
    // Back face
    glTexCoord2f(0.0f, 0.0f); glVertex3f(-width / 2, -height / 2, -depth / 2);
    glTexCoord2f(1.0f, 0.0f); glVertex3f(width / 2, -height / 2, -depth / 2);
    glTexCoord2f(1.0f, 1.0f); glVertex3f(width / 2, height / 2, -depth / 2);
    glTexCoord2f(0.0f, 1.0f); glVertex3f(-width / 2, height / 2, -depth / 2);
    // Top face
    glTexCoord2f(0.0f, 0.0f); glVertex3f(-width / 2, height / 2, -depth / 2);
    glTexCoord2f(1.0f, 0.0f); glVertex3f(width / 2, height / 2, -depth / 2);
    glTexCoord2f(1.0f, 1.0f); glVertex3f(width / 2, height / 2, depth / 2);
    glTexCoord2f(0.0f, 1.0f); glVertex3f(-width / 2, height / 2, depth / 2);
    // Bottom face
    glTexCoord2f(0.0f, 0.0f); glVertex3f(-width / 2, -height / 2, -depth / 2);
    glTexCoord2f(1.0f, 0.0f); glVertex3f(width / 2, -height / 2, -depth / 2);
    glTexCoord2f(1.0f, 1.0f); glVertex3f(width / 2, -height / 2, depth / 2);
    glTexCoord2f(0.0f, 1.0f); glVertex3f(-width / 2, -height / 2, depth / 2);
    // Right face
    glTexCoord2f(0.0f, 0.0f); glVertex3f(width / 2, -height / 2, -depth / 2);
    glTexCoord2f(1.0f, 0.0f); glVertex3f(width / 2, height / 2, -depth / 2);
    glTexCoord2f(1.0f, 1.0f); glVertex3f(width / 2, height / 2, depth / 2);
    glTexCoord2f(0.0f, 1.0f); glVertex3f(width / 2, -height / 2, depth / 2);
    // Left face
    glTexCoord2f(0.0f, 0.0f); glVertex3f(-width / 2, -height / 2, -depth / 2);
    glTexCoord2f(1.0f, 0.0f); glVertex3f(-width / 2, -height / 2, depth / 2);
    glTexCoord2f(1.0f, 1.0f); glVertex3f(-width / 2, height / 2, depth / 2);
    glTexCoord2f(0.0f, 1.0f); glVertex3f(-width / 2, height / 2, -depth / 2);
    glEnd();
}

void Furniture::drawTexturedCylinder(GLfloat radius, GLfloat height, GLint slices, GLint stacks) const 
{
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

void Furniture::drawTable() const 
{
    float top_width = 2.5f;
    float top_depth = 1.5f;
    float top_height = 0.15f;
    float leg_radius = 0.05f;
    float leg_height = 1.2f;

    glPushMatrix();
    glScalef(1.5f, 1.2f, 1.5f);
    glTranslatef(4.0f, -1.2f, -0.5f);
    glBindTexture(GL_TEXTURE_2D, (*texture_ids)["textures/wood.png"]);

    glPushMatrix();
    drawTexturedCube(top_width, top_height, top_depth);
    glPopMatrix();

    glPushMatrix();
    glTranslatef(0.0f, 0.0f, top_height);
    glRotatef(90, 1, 0, 0);

    glPushMatrix();
    glTranslatef(-top_width / 2 + leg_radius, 0.52, 0);
    drawTexturedCylinder(leg_radius, leg_height, 32, 32);
    glPopMatrix();

    glPushMatrix();
    glTranslatef(-top_width / 2 + leg_radius, -0.8, 0);
    drawTexturedCylinder(leg_radius, leg_height, 32, 32);
    glPopMatrix();

    glPushMatrix();
    glTranslatef(top_width / 2 - leg_radius, 0.52, 0);
    drawTexturedCylinder(leg_radius, leg_height, 32, 32);
    glPopMatrix();

    glPushMatrix();
    glTranslatef(top_width / 2 - leg_radius, -0.8, 0);
    drawTexturedCylinder(leg_radius, leg_height, 32, 32);
    glPopMatrix();

    glBindTexture(GL_TEXTURE_2D, 0);
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
    glBindTexture(GL_TEXTURE_2D, (*texture_ids)["textures/metal.jpg"]);
    drawTexturedCylinder(0.15f, 0.4f, 32, 32);
    glBindTexture(GL_TEXTURE_2D, 0);

    glColor3f(0.0f, 0.0f, 0.0f);
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
