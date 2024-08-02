#ifndef TEXTURE_LOADER_H
#define TEXTURE_LOADER_H

#include <GL/freeglut.h>
#include <SOIL2/SOIL2.h>
#include <iostream>
#include <unordered_map>
#include <string>
#include <vector>

extern std::unordered_map<std::string, GLuint>* texture_ids;

GLuint load_texture(const char* filename);
void initialize_textures();

#endif // TEXTURE_LOADER_H