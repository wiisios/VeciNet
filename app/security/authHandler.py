import os
import time
from typing import Dict

from dotenv import load_dotenv
import jwt
from decouple import config
from app.domain import UserResponse

from pathlib import Path
env_path = Path('app.') / '.env'
load_dotenv(dotenv_path=env_path)


JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")


def token_response(token: str):
    return {
        "access_token": token
    }

def sign_jwt(user: UserResponse) -> Dict[str, str]:
    payload = {
        #ver que incluir aca
        "user_id": user.id,
        "role": user.role,
        "email": user.email,
        "expires": time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)

def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        if decoded_token["expires"] >= time.time():
            return decoded_token
        else:
            raise ValueError("Token has expired")
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None