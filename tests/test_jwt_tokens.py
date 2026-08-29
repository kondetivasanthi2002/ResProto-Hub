import unittest
from src.server.jwt_token_manager import JwtTokenManager

class TestJwtTokens(unittest.TestCase):
    def setUp(self):
        self.jwt = JwtTokenManager()

    def test_token_creation(self):
        token = self.jwt.create_token({'user_id': 'admin', 'role': 'RESEARCHER'})
        self.assertEqual(token.count('.'), 2)

if __name__ == '__main__':
    unittest.main()
