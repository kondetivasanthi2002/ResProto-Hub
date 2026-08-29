import unittest
from src.core.metrics.anomaly_drift_detector import AnomalyDriftDetector

class TestAnomalyDrift(unittest.TestCase):
    def setUp(self):
        self.detector = AnomalyDriftDetector(threshold=0.1)

    def test_no_drift(self):
        base = [1.0, 2.0, 3.0, 4.0, 5.0]
        targ = [1.1, 2.1, 3.1, 4.1, 5.1]
        res = self.detector.detect_drift(base, targ)
        self.assertIn('ks_statistic', res)

    def test_drift_detected(self):
        base = [1.0, 2.0, 3.0]
        targ = [10.0, 20.0, 30.0]
        res = self.detector.detect_drift(base, targ)
        self.assertTrue(res['drift_detected'])

if __name__ == '__main__':
    unittest.main()
