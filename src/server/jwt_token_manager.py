import base64
import json
import hashlib
import hmac
import time
from typing import Dict, Any

class JwtTokenManager:
    """
    HMAC-SHA256 JWT session token generator and verifier for RBAC services.
    """
    def __init__(self, secret_key: str = "super_secret_resproto_key"):
        self.secret_key = secret_key.encode('utf-8')

    def _b64url_encode(self, data: bytes) -> str:
        return base64.urlsafe_b64encode(data).rstrip(b'=').decode('utf-8')

    def create_token(self, payload: Dict[str, Any], expires_in: int = 3600) -> str:
        header = {"alg": "HS256", "typ": "JWT"}
        payload_copy = dict(payload)
        payload_copy["exp"] = int(time.time()) + expires_in
        h_str = self._b64url_encode(json.dumps(header).encode('utf-8'))
        p_str = self._b64url_encode(json.dumps(payload_copy).encode('utf-8'))
        sig_input = f"{h_str}.{p_str}".encode('utf-8')
        signature = hmac.new(self.secret_key, sig_input, hashlib.sha256).digest()
        s_str = self._b64url_encode(signature)
        return f"{h_str}.{p_str}.{s_str}"
