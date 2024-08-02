#ifndef FURNITURE_H
#define FURNITURE_H

#include <GL/freeglut.h>
#include <Eigen/Dense>
#include "obb.h"

class Furniture {
public:
    void drawCylinder(float radius, float height, int slices, int stacks) const;
    void drawTable() const;
    void drawTrashCan() const;

    OBB getTableOBB() const;
    OBB getTrashCanOBB() const;
};

#endif // FURNITURE_H