import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()

def decrypt_data(key: bytes, iv: bytes, encrypted_data: bytes, tag: bytes) -> dict:
    decryptor = Cipher(
        algorithms.AES(key),
        modes.GCM(iv, tag),
        backend=default_backend()
    ).decryptor()
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
    return json.loads(decrypted_data)

class DecodeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        if request.method in ("POST", "PUT", "PATCH"):
            body = await request.body()
            try:
                if request.method in ("POST", "PUT" ) and request.headers.get("Authorization"):
                    encrypted_payload = json.loads(body)
                    iv = bytes(encrypted_payload['iv'])
                    data = bytes(encrypted_payload['data'])
                    tag = bytes(encrypted_payload['tag'])

                    key = b'yourSharedSecretKey'[:16]
                    decrypted_data = decrypt_data(key, iv, data, tag)
                    request._body = json.dumps(decrypted_data).encode('utf-8')
            except Exception as e:

                return JSONResponse(
                    status_code=400,
                    content={"message": "Invalid encrypted data", "detail": str(e)}
                )

        response = await call_next(request)
        return response
    