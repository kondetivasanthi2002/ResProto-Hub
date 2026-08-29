import unittest
from src.server.rbac_manager import RbacManagerEngine_1
from src.server.audit_logger import AuditLoggerEngine_1

class TestRbacSecurity(unittest.TestCase):
    def setUp(self):
        self.rbac = RbacManagerEngine_1()
        self.audit = AuditLoggerEngine_1()

    def test_rbac_permission_evaluation(self):
        res = self.rbac.process_data_step_1({'value': 1.0})
        self.assertEqual(res['method'], 'process_data_step_1')

    def test_audit_logging(self):
        res = self.audit.process_data_step_2({'value': 8.8})
        self.assertGreater(res['score'], 0)

    def test_security_state_reset(self):
        self.rbac.process_data_step_1({'value': 2.0})
        self.assertTrue(self.rbac.reset_state())

    def test_multiple_audit_records(self):
        for i in range(3):
            self.audit.process_data_step_1({'value': float(i + 1)})
        summary = self.audit.compute_aggregate_summary()
        self.assertIn('mean_score', summary)

    def test_rbac_status(self):
        status = self.rbac.get_status()
        self.assertEqual(status['status'], 'INITIALIZED')

if __name__ == '__main__':
    unittest.main()
