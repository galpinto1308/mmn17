#ifndef OBB_H
#define OBB_H

#include <Eigen/Dense>
#include <vector>

class OBB {
public:
    Eigen::Vector3f center;
    Eigen::Vector3f half_sizes;
    Eigen::Matrix3f orientation;

    OBB(const Eigen::Vector3f& center, const Eigen::Vector3f& half_sizes, const Eigen::Matrix3f& orientation)
        : center(center), half_sizes(half_sizes), orientation(orientation) {}

    bool intersects(const OBB& other) const;
    OBB combine(const OBB& other) const;
    std::vector<Eigen::Vector3f> getCorners() const;

private:
    static bool obbIntersects(const OBB& obb1, const OBB& obb2);
    static bool overlapOnAxis(const OBB& obb1, const OBB& obb2, const Eigen::Vector3f& axis);
    static std::pair<float, float> projectOBB(const OBB& obb, const Eigen::Vector3f& axis);
};

#endif // OBB_H
