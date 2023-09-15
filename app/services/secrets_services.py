import os

from isodate import parse_duration

from app.models.secrets import SecretCreate, SecretBase
from app.services.encode_services import get_encoded_pass_key, encode_content


def create_secret_model(secret: SecretCreate, pass_key_lifetime: str) -> SecretBase:
    encoded_key = get_encoded_pass_key(
        data={"sub": dict(secret).get("pass_key")},
        expires_delta=parse_duration(pass_key_lifetime)
    )
    encoded_content = encode_content(
        data={"sub": dict(secret).get("content")},
        encode_key=dict(secret).get("pass_key")
    )
    new_secret = SecretBase(
        encoded_pass_key=encoded_key, encoded_content=encoded_content,
        link=f'{os.getenv("APP_URL")}/secrets/read/{encoded_key}', pass_key_lifetime=pass_key_lifetime
    )
    return new_secret
