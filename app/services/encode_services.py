import os
from datetime import timedelta, datetime

from dotenv import load_dotenv
from fastapi import status
from fastapi.exceptions import HTTPException
from jose import jwt, JWTError, ExpiredSignatureError
from passlib.context import CryptContext

load_dotenv()
ENCODE_ALGORITHM = "HS256"
SECRET_KEY = os.getenv("SECRET_KEY")

crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_encoded_pass_key(data: dict, expires_delta: timedelta) -> str:
    """
    Encodes the pass_key via the jose.jwt.encode() method.
    The pass_key of a new secret is used as the 'key' encode method's parameter and the 'sub' part of the payload.
    :param data: Takes a dict() 'data' of type {"sub": "<value to be encoded as the 'sub' part of the payload >"}
    :param expires_delta: pass key lifetime to be set as the 'exp' parameter of the encoded data.
    :return: encoded pass key
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_pass_key = jwt.encode(to_encode, key=SECRET_KEY, algorithm=ENCODE_ALGORITHM)
    return encoded_pass_key


def encode_content(data: dict) -> str:
    """
    Encodes the content of a secret via the jose.jwt.encode() method.
    :return: encoded pass key
    :param data: Takes a dict() 'data' of type {"sub": "<value of the secret's content>"}
    :return: encoded content
    """
    to_encode = data.copy()
    encoded_content = jwt.encode(to_encode, key=SECRET_KEY, algorithm=ENCODE_ALGORITHM)
    return encoded_content


def decode_data(encoded_content: str) -> str:
    """
    Decodes data via the jose.jwt.decode() method.
    :param encoded_content: encoded data.
    :return: decoded data stored as the 'sub' keys value in decoded payloads.
    """
    try:
        payload = jwt.decode(encoded_content, key=SECRET_KEY, algorithms=ENCODE_ALGORITHM)
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your pass key has expired!",
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either encoded_pass_key or pass_key are invalid!",
        )
    return payload.get("sub")
