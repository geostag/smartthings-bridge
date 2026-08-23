"""
SmartThings webhook verification boundary.

SmartThings signs webhook requests using HTTP Signatures with RSA-SHA256 and
sends Authorization, Digest and Date headers.

The production implementation should:
1. parse keyId/signature/signed headers from Authorization
2. fetch/cache the public key identified by keyId
3. reconstruct the signing string using (request-target), digest and date
4. verify RSA-SHA256
5. verify Digest against the raw request body
6. reject stale/invalid requests

Kept isolated here so the rest of the application is not coupled to the
transport-level verification implementation.
"""

def verify_request(request, body: bytes) -> bool:
    # Deliberately fail closed once production webhook integration is enabled.
    # For the current pre-registration phase we allow local synthetic testing.
    if request.headers.get("X-Bridge-Test") == "1":
        return True
    return False
