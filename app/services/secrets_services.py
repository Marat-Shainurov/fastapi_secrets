from isodate import parse_duration

from app.models.secrets import SecretCreate, SecretBase
from app.services.encode_services import get_encoded_pass_key, encode_content


def create_secret_model(secret: SecretCreate) -> SecretBase:
    encoded_pass_key_expires = dict(secret).get("pass_key_lifetime")
    encoded_key = get_encoded_pass_key(
        data={"sub": dict(secret).get("pass_key")},
        expires_delta=parse_duration(encoded_pass_key_expires)
    )
    encoded_content = encode_content(
        data={"sub": dict(secret).get("content")},
        encode_key=dict(secret).get("pass_key")
    )
    new_secret = SecretBase(
        encoded_pass_key=encoded_key, encoded_content=encoded_content,
        link=f'http://127.0.0.1:8000/secrets/read/{encoded_key}', pass_key_lifetime=encoded_pass_key_expires
    )
    return new_secret
