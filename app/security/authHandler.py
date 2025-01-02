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

#Obtaining JWT data to generate it
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")

# Dict that contains JWtoken
def token_response(token: str):
    return {
        "access_token": token
    }

# Generating JWtoken with selected information
def sign_jwt(user: UserResponse) -> Dict[str, str]:
    payload = {
        "user_id": user.id,
        "role": user.role,
        "email": user.email,
        "expires": time.time() + 60000
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)

# Function to decode the JWToken
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