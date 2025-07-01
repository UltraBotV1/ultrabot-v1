# utils.py

import time
import hmac
import hashlib

def get_timestamp():
    return str(int(time.time() * 1000))

def sign_request(secret_key, params):
    """
    Signs request using HMAC SHA256 as required by BloFin for private endpoints.
    Expects `params` as a string of sorted query params.
    """
    signature = hmac.new(
        secret_key.encode("utf-8"),
        params.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()
    return signature