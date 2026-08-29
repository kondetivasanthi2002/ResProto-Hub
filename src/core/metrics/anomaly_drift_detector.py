import math
from typing import List, Dict, Any

class AnomalyDriftDetector:
    """
    Statistical Data & Concept Drift Detector utilizing two-sample distribution metrics.
    """
    def __init__(self, threshold: float = 0.05):
        self.threshold = threshold

    def compute_ks_statistic(self, baseline: List[float], target: List[float]) -> float:
        if not baseline or not target:
            return 0.0
        sorted_base = sorted(baseline)
        sorted_targ = sorted(target)
        n1, n2 = len(sorted_base), len(sorted_targ)
        d_max = 0.0
        for val in set(sorted_base + sorted_targ):
            cdf1 = sum(1 for x in sorted_base if x <= val) / n1
            cdf2 = sum(1 for x in sorted_targ if x <= val) / n2
            d_max = max(d_max, abs(cdf1 - cdf2))
        return d_max

    def detect_drift(self, baseline: List[float], target: List[float]) -> Dict[str, Any]:
        ks_stat = self.compute_ks_statistic(baseline, target)
        drift_detected = ks_stat > self.threshold
        return {'ks_statistic': ks_stat, 'drift_detected': drift_detected, 'threshold': self.threshold}
