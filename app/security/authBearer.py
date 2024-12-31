import time
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .authHandler import decode_jwt


class JWTBearer(HTTPBearer):
    def __init__(self, allowed_roles: list, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)
        self.allowed_roles = allowed_roles

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if credentials.scheme != "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            
            payload = self.verify_jwt(credentials.credentials)
            if not payload:
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            
            if not self.has_roles(payload, self.allowed_roles):
                raise HTTPException(status_code=403, detail="Insufficient permissions.")
            
            return payload
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> dict:
        try:
            payload = decode_jwt(jwtoken)
            if payload and payload.get("expires", 0) >= time.time():
                return payload
        except Exception as e:
            print(f"JWT verification failed: {e}")
        return None
    
    def has_roles(self, decoded_token: dict, allowed_roles: list) -> bool:
        return decoded_token.get("role") in allowed_roles