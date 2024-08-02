#include "obb.h"
#include <Eigen/Dense>

bool OBB::intersects(const OBB& other) const {
    return obbIntersects(*this, other);
}

OBB OBB::combine(const OBB& other) const {
    std::vector<Eigen::Vector3f> points1 = getCorners();
    std::vector<Eigen::Vector3f> points2 = other.getCorners();
    points1.insert(points1.end(), points2.begin(), points2.end());

    Eigen::Vector3f new_center = Eigen::Vector3f::Zero();
    for (const auto& point : points1) {
        new_center += point;
    }
    new_center /= points1.size();

    Eigen::Matrix3f new_orientation = Eigen::Matrix3f::Identity(); // Simplified orientation
    Eigen::Vector3f min_point = points1[0];
    Eigen::Vector3f max_point = points1[0];

    for (const auto& point : points1) {
        min_point = min_point.cwiseMin(point);
        max_point = max_point.cwiseMax(point);
    }

    Eigen::Vector3f new_half_sizes = (max_point - min_point) / 2.0f;

    return OBB(new_center, new_half_sizes, new_orientation);
}

std::vector<Eigen::Vector3f> OBB::getCorners() const {
    std::vector<Eigen::Vector3f> corners;
    for (int dx = -1; dx <= 1; dx += 2) {
        for (int dy = -1; dy <= 1; dy += 2) {
            for (int dz = -1; dz <= 1; dz += 2) {
                Eigen::Vector3f corner = center 
                                       + dx * half_sizes[0] * orientation.col(0)
                                       + dy * half_sizes[1] * orientation.col(1)
                                       + dz * half_sizes[2] * orientation.col(2);
                corners.push_back(corner);
            }
        }
    }
    return corners;
}

bool OBB::obbIntersects(const OBB& obb1, const OBB& obb2) {
    std::vector<Eigen::Vector3f> axes;

    axes.push_back(obb1.orientation.col(0));
    axes.push_back(obb1.orientation.col(1));
    axes.push_back(obb1.orientation.col(2));
    axes.push_back(obb2.orientation.col(0));
    axes.push_back(obb2.orientation.col(1));
    axes.push_back(obb2.orientation.col(2));

    for (int i = 0; i < 3; ++i) {
        for (int j = 0; j < 3; ++j) {
            axes.push_back(obb1.orientation.col(i).cross(obb2.orientation.col(j)).normalized());
        }
    }

    for (const auto& axis : axes) {
        if (!overlapOnAxis(obb1, obb2, axis)) {
            return false;
        }
    }

    return true;
}

bool OBB::overlapOnAxis(const OBB& obb1, const OBB& obb2, const Eigen::Vector3f& axis) {
    auto projection1 = projectOBB(obb1, axis);
    auto projection2 = projectOBB(obb2, axis);
    return projection1.first <= projection2.second && projection2.first <= projection1.second;
}

std::pair<float, float> OBB::projectOBB(const OBB& obb, const Eigen::Vector3f& axis) {
    float center_projection = obb.center.dot(axis);
    float half_size_projection = 0.0f;

    for (int i = 0; i < 3; ++i) {
        half_size_projection += obb.half_sizes[i] * std::abs(obb.orientation.col(i).dot(axis));
    }

    return std::make_pair(center_projection - half_size_projection, center_projection + half_size_projection);
}
