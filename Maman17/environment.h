#ifndef ENVIRONMENT_H
#define ENVIRONMENT_H

#include <vector>
#include "obb.h"
#include "texture_loader.h"

class Environment {
public:
    std::vector<OBB> wall_obbs;

    Environment(int rows, int columns, float size, float wall_height);
    void drawCheckerboard();
    void drawWalls();
    void createWallObbs();

private:
    int rows;
    int columns;
    float size;
    float wall_height;
};

#endif // ENVIRONMENT_H