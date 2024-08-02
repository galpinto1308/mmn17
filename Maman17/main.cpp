#include "main.h"
#include "lib/imgui-master/imgui.h"
#include "lib/imgui-master/backends/imgui_impl_glut.h"
#include "lib/imgui-master/backends/imgui_impl_opengl2.h"
#include <cmath>
#include <ctime>
using namespace std;

int window_width = 1280;
int window_height = 860;

// Light default variables
float ambient_factor = 0.6f;
float lamp_intensity = 1.0f;
Eigen::Vector3f lamp_position(4.0f, 5.0f, -1.0f);
Eigen::Vector3f lamp_direction(4.0f, 0.0f, -1.0f);

// Scene flags
bool move_flag = false;
bool robot_view = false;
bool lamp_flag = false;
bool lamp_dir_flag = false;
bool lamp_int_flag = false;

// State to keep track of which keys are pressed
unordered_map<char, bool> keys = { {'a', false}, {'d', false}, {'w', false}, {'s', false} };

Robot robot;
Environment environment(20, 20, 2.0f, 8.0f);
Furniture furniture;
Camera camera(Eigen::Vector3f(0.0f, 1.0f, 10.0f), 6.0f, 2.0f);

void cleanFlags()
{
    robot_view = false;
    lamp_flag = false;
    lamp_dir_flag = false;
    lamp_int_flag = false;
    move_flag = false;
}

bool show_help_window = false;
void menu()
{
    // Create a new ImGui frame
    ImGui_ImplOpenGL2_NewFrame();
    ImGui_ImplGLUT_NewFrame();
    ImGui::NewFrame();

    // Set size constraints for the control panel window
    ImGui::SetNextWindowSizeConstraints(ImVec2(400, 300), ImVec2(FLT_MAX, FLT_MAX));

    // Create a new ImGui window
    ImGui::Begin("Control Panel");

    // Begin a child window to enable scrolling
    ImGui::BeginChild("ScrollingRegion", ImVec2(0, 300), true, ImGuiWindowFlags_HorizontalScrollbar);

    // Light subcategory
    if (ImGui::CollapsingHeader("Light")) {
        ImGui::SliderFloat("Ambient Light", &ambient_factor, 0.0f, 1.0f);
        ImGui::SliderFloat("Lamp Intensity", &lamp_intensity, 0.0f, 2.0f);
        ImGui::SliderFloat3("Lamp Position", &lamp_position[0], -10.0f, 10.0f);
        ImGui::SliderFloat3("Lamp Direction", &lamp_direction[0], -10.0f, 10.0f);
    }

    // Camera subcategory
    if (ImGui::CollapsingHeader("Camera")) {
        ImGui::Checkbox("Robot View", &robot_view);
        ImGui::SliderFloat("Camera Distance", &camera.distance, 1.0f, 100.0f);
        ImGui::SliderFloat("Camera Angle X", &camera.angle_x, 0.0f, 180.0f);
        ImGui::SliderFloat("Camera Angle Y", &camera.angle_y, -180.0f, 180.0f);
    }

    // Robot Angles subcategory
    if (ImGui::CollapsingHeader("Robot Angles")) {
        ImGui::SliderFloat("Shoulder Angle", &robot.shoulder_angle, -180.0f, 180.0f);
        ImGui::SliderFloat("Elbow Angle", &robot.elbow_angle, -31.0f, 0.0f);  // Adjusted range for elbow
        ImGui::SliderFloat("Hand Angle", &robot.hand_angle, -180.0f, 180.0f);
        ImGui::SliderFloat("Head Angle", &robot.head_angle, -180.0f, 180.0f);
        ImGui::SliderFloat("Rotation Angle", &robot.rotation_angle_all, -180.0f, 180.0f);
    }

    // End the child window
    ImGui::EndChild();

    // Add some space before the help button
    ImGui::SetCursorPosY(ImGui::GetCursorPosY() + 10);

    // Help button
    if (ImGui::Button("Help", ImVec2(ImGui::GetContentRegionAvail().x, 0))) {
        show_help_window = true;
    }

    // End the ImGui window
    ImGui::End();

    // Show help window if the help button is pressed
    if (show_help_window) {
        ImGui::SetNextWindowSize(ImVec2(400, 300));
        ImGui::Begin("Help", &show_help_window);

        ImGui::Text("Controls:");
        ImGui::BulletText("W, A, S, D: Move the robot");

        ImGui::Separator();

        ImGui::Text("Control Panel:");
        ImGui::BulletText("Light: Adjust ambient light and lamp settings");
        ImGui::BulletText("Camera: Adjust camera view settings");
        ImGui::BulletText("Robot Angles: Adjust the robot's joint angles");

        ImGui::End();
    }

    // Render ImGui
    ImGui::Render();
    ImGui_ImplOpenGL2_RenderDrawData(ImGui::GetDrawData());
}

void myDisplay() {
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    glLoadIdentity();

    if (robot_view) {
        Eigen::Vector3f eye_offset(0.0f, 0.68f, 0.25f);
        Eigen::Vector3f target_offset(0.0f, 0.0f, 5.0f);

        float rotation_angle_rad = (robot.rotation_angle_all + robot.head_angle) * PI / 180.0f;

        float eye_x = eye_offset[0] * cos(rotation_angle_rad) + eye_offset[2] * sin(rotation_angle_rad);
        float eye_z = eye_offset[2] * cos(rotation_angle_rad) - eye_offset[0] * sin(rotation_angle_rad);
        Eigen::Vector3f eye_position = robot.pos + Eigen::Vector3f(eye_x, eye_offset[1], eye_z);

        float target_x = target_offset[0] * cos(rotation_angle_rad) + target_offset[2] * sin(rotation_angle_rad);
        float target_z = target_offset[2] * cos(rotation_angle_rad) - target_offset[0] * sin(rotation_angle_rad);
        Eigen::Vector3f target_position = robot.pos + Eigen::Vector3f(target_x, 0.0f, target_z);

        gluLookAt(eye_position[0], eye_position[1], eye_position[2],
            target_position[0], target_position[1], target_position[2], 0.0f, 1.0f, 0.0f);
    }
    else {
        gluLookAt(robot.pos[0] + camera.distance * sin(camera.angle_y * PI / 180.0f) * cos(camera.angle_x * PI / 180.0f),
            robot.pos[1] + camera.distance * sin(camera.angle_x * PI / 180.0f),
            robot.pos[2] + camera.distance * cos(camera.angle_y * PI / 180.0f) * cos(camera.angle_x * PI / 180.0f),
            robot.pos[0], robot.pos[1], robot.pos[2], 0.0f, 1.0f, 0.0f);
    }

    lighting();
    environment.drawCheckerboard();
    environment.drawWalls();
    robot.draw();
    furniture.drawTable();
    furniture.drawTrashCan();

    menu();

    glutSwapBuffers();
    glFlush();
}

void myReshape(int width, int height)
{
    if (height == 0) {
        height = 1;
    }
    float aspect = static_cast<float>(width) / height;

    glViewport(0, 0, width, height);

    window_width = width;
    window_height = height;

    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluPerspective(45.0, aspect, 0.1, 100.0);

    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();

    // Update ImGui display size
    ImGuiIO& io = ImGui::GetIO();
    io.DisplaySize = ImVec2(static_cast<float>(width), static_cast<float>(height));
}

void lighting() {
    glEnable(GL_LIGHTING);
    glEnable(GL_COLOR_MATERIAL);
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE);
    GLfloat ambient_light[] = { ambient_factor, ambient_factor, ambient_factor, 1.0f };
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, ambient_light);

    glEnable(GL_LIGHT1);
    GLfloat lamp_light_intensity[] = { lamp_intensity, lamp_intensity, lamp_intensity, 1.0f };
    GLfloat lamp_light_position[] = { lamp_position[0], lamp_position[1], lamp_position[2], 1.0f };
    GLfloat direction[] = { lamp_direction[0] - lamp_position[0], lamp_direction[1] - lamp_position[1], lamp_direction[2] - lamp_position[2] };
    GLfloat cutoff = 90.0f;
    GLfloat exponent = 0.0f;

    glLightfv(GL_LIGHT1, GL_POSITION, lamp_light_position);
    glLightfv(GL_LIGHT1, GL_DIFFUSE, lamp_light_intensity);
    glLightfv(GL_LIGHT1, GL_SPECULAR, lamp_light_intensity);
    glLightfv(GL_LIGHT1, GL_SPOT_DIRECTION, direction);
    glLightf(GL_LIGHT1, GL_SPOT_CUTOFF, cutoff);
    glLightf(GL_LIGHT1, GL_SPOT_EXPONENT, exponent);
}

float clamp(float value, float min, float max) {
    if (value < min) return min;
    if (value > max) return max;
    return value;
}

void updateMove(unsigned char key, int x, int y) {
    switch (key) {
    case 'a':
        keys['a'] = true;
        break;
    case 'd':
        keys['d'] = true;
        break;
    case 'w':
        keys['w'] = true;
        break;
    case 's':
        keys['s'] = true;
        break;
    }

    updateVelocity();
}

void keyRelease(unsigned char key, int x, int y)
{
    switch (key) {
    case 'a':
        keys['a'] = false;
        break;
    case 'd':
        keys['d'] = false;
        break;
    case 'w':
        keys['w'] = false;
        break;
    case 's':
        keys['s'] = false;
        break;
    }

    updateVelocity();
}

void updateVelocity() 
{
    float rad_y = camera.angle_y * PI / 180.0f;
    Eigen::Vector3f forward(cos(rad_y), 0, sin(rad_y));
    Eigen::Vector3f right(-sin(rad_y), 0, cos(rad_y));

    Eigen::Vector3f velocity = Eigen::Vector3f::Zero();

    if (keys['w']) velocity -= right;
    if (keys['s']) velocity += right;
    if (keys['a']) velocity -= forward;
    if (keys['d']) velocity += forward;

    robot.velocity = velocity.normalized() * robot.speed;
}

void timer(int value)
{
    static float last_time = static_cast<float>(clock()) / CLOCKS_PER_SEC;
    float current_time = static_cast<float>(clock()) / CLOCKS_PER_SEC;
    float dt = current_time - last_time;
    last_time = current_time;

    OBB robot_bb = robot.getOBB();
    OBB table_bb = furniture.getTableOBB();
    OBB trash_can_bb = furniture.getTrashCanOBB();

    Eigen::Vector3f new_pos = robot.pos + robot.velocity * dt;

    float new_rotation_angle_all = (robot.velocity[0] != 0 || robot.velocity[2] != 0)
        ? atan2(robot.velocity[0], robot.velocity[2]) * 180.0f / PI
        : robot.rotation_angle_all;

    float angle_rad = new_rotation_angle_all * PI / 180.0f;
    Eigen::Matrix3f rotation_matrix;
    rotation_matrix << cos(angle_rad), 0, -sin(angle_rad),
        0, 1, 0,
        sin(angle_rad), 0, cos(angle_rad);

    OBB new_robot_bb(new_pos, robot_bb.half_sizes, rotation_matrix);

    bool collision = new_robot_bb.intersects(table_bb) || new_robot_bb.intersects(trash_can_bb) ||
        any_of(environment.wall_obbs.begin(), environment.wall_obbs.end(), [&](const OBB& wall) { return new_robot_bb.intersects(wall); });

    if (!collision) {
        robot.pos = new_pos;
        if (robot.velocity[0] != 0 || robot.velocity[2] != 0) {
            robot.rotation_angle_all = atan2(robot.velocity[0], robot.velocity[2]) * 180.0f / (float)PI;
        }
    }
    else {
        robot.velocity = Eigen::Vector3f::Zero();
    }

    glutPostRedisplay();
    glutTimerFunc(16, timer, 0);
}



int main(int argc, char** argv) {
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH | GLUT_MULTISAMPLE);
    glutInitWindowSize(window_width, window_height);
    glutInitWindowPosition(0, 0);
    int window = glutCreateWindow("Robot Environment Simulation");

    glEnable(GL_TEXTURE_2D);
    glEnable(GL_DEPTH_TEST);
    glDepthFunc(GL_LEQUAL);
    glShadeModel(GL_SMOOTH);
    glEnable(GL_NORMALIZE);
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST);

    glEnable(GL_LINE_SMOOTH);
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST);
    glEnable(GL_POLYGON_SMOOTH);
    glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST);

    // Setup ImGui context
    IMGUI_CHECKVERSION();
    ImGui::CreateContext();
    ImGuiIO& io = ImGui::GetIO(); (void)io;
    ImGui::StyleColorsDark();

    // Setup Platform/Renderer bindings
    ImGui_ImplGLUT_Init();
    ImGui_ImplGLUT_InstallFuncs();
    ImGui_ImplOpenGL2_Init();

    initialize_textures();
    environment.createWallObbs();
    glutDisplayFunc(myDisplay);
    glutKeyboardFunc(updateMove);
    glutKeyboardUpFunc(keyRelease);
    glutReshapeFunc(myReshape);
    glutTimerFunc(16, timer, 0);
    glutMainLoop();

    // Cleanup
    ImGui_ImplOpenGL2_Shutdown();
    ImGui_ImplGLUT_Shutdown();
    ImGui::DestroyContext();
    delete(texture_ids);

    return 0;
}
