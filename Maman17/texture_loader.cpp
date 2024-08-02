#include "texture_loader.h"

std::unordered_map<std::string, GLuint>* texture_ids;

GLuint load_texture(const char* filename) 
{
    GLuint texture = SOIL_load_OGL_texture(
        filename,
        SOIL_LOAD_AUTO,
        SOIL_CREATE_NEW_ID,
        SOIL_FLAG_MIPMAPS | SOIL_FLAG_INVERT_Y | SOIL_FLAG_NTSC_SAFE_RGB | SOIL_FLAG_COMPRESS_TO_DXT
    );

    if (texture == 0) {
        std::cerr << "SOIL loading error: '" << SOIL_last_result() << "' (" << filename << ")" << std::endl;
    }

    glBindTexture(GL_TEXTURE_2D, texture);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
    glBindTexture(GL_TEXTURE_2D, 0);

    return texture;
}

void initialize_textures() 
{
    std::vector<std::string> images_to_load = { "textures/walls.jpg", "textures/wood.png", "textures/metal.jpg", "textures/robot_texture.jpg" };
    texture_ids = new std::unordered_map<std::string, GLuint>(images_to_load.size());
    for (const auto& image : images_to_load)
        (*texture_ids)[image] = load_texture(image.c_str());
    
}
