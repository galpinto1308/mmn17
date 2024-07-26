import numpy as np

class OBB:
    def __init__(self, center, half_sizes, orientation):
        self.center = np.array(center)
        self.half_sizes = np.array(half_sizes)
        self.orientation = np.array(orientation)  # 3x3 rotation matrix

    def intersects(self, other):
        return self.obb_intersects(self, other)

    def combine(self, other):
        points1 = self.get_corners()
        points2 = other.get_corners()
        all_points = np.vstack((points1, points2))

        new_center = np.mean(all_points, axis=0)
        new_orientation = np.eye(3)  # Simplified; you can use a more complex method to combine orientations
        new_half_sizes = (np.max(all_points, axis=0) - np.min(all_points, axis=0)) / 2

        return OBB(new_center, new_half_sizes, new_orientation)

    def get_corners(self):
        corners = []
        for dx in [-1, 1]:
            for dy in [-1, 1]:
                for dz in [-1, 1]:
                    corner = self.center + dx * self.half_sizes[0] * self.orientation[:, 0] \
                                      + dy * self.half_sizes[1] * self.orientation[:, 1] \
                                      + dz * self.half_sizes[2] * self.orientation[:, 2]
                    corners.append(corner)
        return np.array(corners)

    @staticmethod
    def obb_intersects(obb1, obb2):
        axes = np.vstack((obb1.orientation, obb2.orientation))
        axes = np.vstack((axes, np.cross(obb1.orientation, obb2.orientation)))
        axes = np.unique(axes, axis=0)  # Remove duplicate axes from cross products

        for axis in axes:
            if not OBB.overlap_on_axis(obb1, obb2, axis):
                return False
        return True

    @staticmethod
    def overlap_on_axis(obb1, obb2, axis):
        projection1 = OBB.project_obb(obb1, axis)
        projection2 = OBB.project_obb(obb2, axis)
        return projection1[0] <= projection2[1] and projection2[0] <= projection1[1]

    @staticmethod
    def project_obb(obb, axis):
        center_projection = np.dot(obb.center, axis)
        half_size_projection = np.sum(np.abs(np.dot(obb.half_sizes * obb.orientation, axis)))
        return [center_projection - half_size_projection, center_projection + half_size_projection]
