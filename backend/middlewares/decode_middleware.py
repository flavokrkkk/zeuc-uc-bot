from copy import deepcopy
import json
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import _StreamingResponse, BaseHTTPMiddleware


class DecodeEncodeMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, dispatch=None):
        super().__init__(app, dispatch)
        self.key = b"9fGDzagmHOCYEvjw"[:16]

    def decrypt_data(self, iv: bytes, encrypted_data: bytes, tag: bytes) -> dict:
        decryptor = Cipher(
            algorithms.AES(self.key),
            modes.GCM(iv, tag),
            backend=default_backend()
        ).decryptor()
        decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
        return json.loads(decrypted_data)

    async def dispatch(self, request, call_next):
        if request.method in ("POST", "PUT", "PATCH"):
            body = await request.body() 
            try:
                if body and not request.url.path.startswith("/api/auth") and not request.url.path.endswith("/callback"):
                    encrypted_payload = json.loads(body)
                    iv = bytes(encrypted_payload["iv"])
                    data = bytes(encrypted_payload["data"])
                    tag = bytes(encrypted_payload["tag"])

                    decrypted_data = self.decrypt_data(iv, data, tag)
                    request._body = json.dumps(decrypted_data).encode("utf-8")
            except Exception as e:
                return JSONResponse(
                    status_code=400,
                    content={"message": "Invalid encrypted data", "detail": str(e)}
                )
            
        response = await call_next(request)

        if response.status_code == 200 and response.headers.get("Content-Type") == "application/json":
            response_body = b""
            async for chunk in response.body_iterator:
                response_body += chunk

            response_data = json.loads(response_body)
            iv = os.urandom(12)
            encryptor = Cipher(
                algorithms.AES(self.key),
                modes.GCM(iv),
                backend=default_backend()
            ).encryptor()
            encoded_data = json.dumps(response_data).encode("utf-8")
            encrypted_data = encryptor.update(encoded_data) + encryptor.finalize()
            encrypted_body = {
                "iv": list(iv),
                "data": list(encrypted_data),
                "tag": list(encryptor.tag)
            }
            async def encrypted_body_iterator():
                yield json.dumps(encrypted_body).encode("utf-8")
            del response.headers["Content-Length"]

            response.body_iterator = encrypted_body_iterator()
        return response