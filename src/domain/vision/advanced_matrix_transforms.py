import math
from typing import List

class VisionMatrixTransformer:
    """
    Applies affine transforms, spatial rotations, and channel normalization.
    """
    def rotate_2d_vector(self, x: float, y: float, angle_rad: float) -> tuple:
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        x_rot = x * cos_a - y * sin_a
        y_rot = x * sin_a + y * cos_a
        return (x_rot, y_rot)

    def normalize_channels(self, matrix: List[List[float]], mean: float = 0.5, std: float = 0.5) -> List[List[float]]:
        return [[(val - mean) / std for val in row] for row in matrix]
