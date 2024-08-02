#ifndef FURNITURE_H
#define FURNITURE_H

#define PI 3.14159265358979323846

#include <GL/freeglut.h>
#include <Eigen/Dense>
#include "obb.h"
#include "texture_loader.h"

class Furniture {
public:
    void drawTable() const;
    void drawTrashCan() const;

    OBB getTableOBB() const;
    OBB getTrashCanOBB() const;
private:
    void drawTexturedCube(float width, float height, float depth) const;
    void drawTexturedCylinder(GLfloat radius, GLfloat height, GLint slices, GLint stacks) const;
};

#endif // FURNITURE_H