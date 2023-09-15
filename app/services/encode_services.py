from datetime import timedelta, datetime

from fastapi import status
from fastapi.exceptions import HTTPException
from jose import jwt, JWTError, ExpiredSignatureError
from passlib.context import CryptContext

ENCODE_ALGORITHM = "HS256"

crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_encoded_pass_key(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    secret_encode_key = data["sub"]
    encoded_pass_key = jwt.encode(to_encode, key=secret_encode_key, algorithm=ENCODE_ALGORITHM)
    return encoded_pass_key


def encode_content(data: dict, encode_key: str) -> str:
    to_encode = data.copy()
    secret_encode_key = encode_key
    encoded_content = jwt.encode(to_encode, key=secret_encode_key, algorithm=ENCODE_ALGORITHM)
    return encoded_content


def decode_data(encoded_content, secret_encode_key) -> str:
    try:
        payload = jwt.decode(encoded_content, key=secret_encode_key, algorithms=ENCODE_ALGORITHM)
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Your pass key has expired!",
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not validate provided data",
        )
    return payload.get("sub")
