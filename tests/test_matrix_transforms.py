import unittest
import math
from src.domain.vision.advanced_matrix_transforms import VisionMatrixTransformer

class TestMatrixTransforms(unittest.TestCase):
    def setUp(self):
        self.transformer = VisionMatrixTransformer()

    def test_rotation(self):
        xr, yr = self.transformer.rotate_2d_vector(1.0, 0.0, math.pi / 2)
        self.assertAlmostEqual(xr, 0.0, places=5)
        self.assertAlmostEqual(yr, 1.0, places=5)

    def test_normalization(self):
        mat = [[0.5, 1.0], [0.0, 0.5]]
        norm = self.transformer.normalize_channels(mat, mean=0.5, std=0.5)
        self.assertEqual(norm[0][0], 0.0)

if __name__ == '__main__':
    unittest.main()
