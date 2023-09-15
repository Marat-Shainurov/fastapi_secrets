from bson import ObjectId
from fastapi import APIRouter, Query, Path
from fastapi.exceptions import HTTPException
from starlette import status

from app.database.config import db
from app.models.enums import PassKeyLifetimeEnum
from app.models.secrets import SecretBase, SecretCreate
from app.schemas.serializers import serializerDict
from app.services.encode_services import decode_data
from app.services.secrets_services import create_secret_model

secrets = APIRouter()


@secrets.post("/secrets/generate", response_model=SecretBase, status_code=status.HTTP_201_CREATED)
async def create_secret(
        secret: SecretCreate,
        pass_key_lifetime: PassKeyLifetimeEnum = Query(
            ..., description="Pass key lifetime. One day by default")):
    """
    Endpoint creates a new secret:
    - **pass_key_lifetime**: each secret must have its lifetime (1 day (P1D in ISO format) as the default value).
    - **content**: each secret has its content(must be longer than 1 symbol).
    - **pass_key**: each secret must have a pass_key, which is used for the content and pass_key encoding,
    and should be used for the secret's reading.
    """
    new_secret = create_secret_model(secret, pass_key_lifetime.value)
    result = db.secrets.insert_one(dict(new_secret))
    created_secret = db.secrets.find_one({"_id": ObjectId(result.inserted_id)})
    created_secret_dict = serializerDict(created_secret)
    return created_secret_dict


@secrets.get("/secrets/read/{encoded_pass_key}")
async def read_secret(
        pass_key: str = Query(..., description="Key to be verified and checked against the pass key of the secret"),
        encoded_pass_key: str = Path(..., description="Encoded pass key")
):
    """
    Endpoint for reading secrets:
    - **encoded_pass_key**: encoded_pass_key of the secret.
    - **pass_key**: pass_key previously set for the secret during its creation.
    """
    secret = db.secrets.find_one({"encoded_pass_key": encoded_pass_key})
    decoded_pass_key = decode_data(encoded_pass_key, secret_encode_key=pass_key)
    if secret and decoded_pass_key == pass_key:
        if not secret.get("is_active"):
            raise HTTPException(
                detail="The secret has been read already!",
                status_code=status.HTTP_403_FORBIDDEN
            )
        else:
            decoded_content = decode_data(dict(secret).get("encoded_content"), secret_encode_key=pass_key)
            db.secrets.find_one_and_update({"_id": ObjectId(secret.get("_id"))},
                                           {"$set": {"is_active": False, "encoded_content": None}})
            return {"secret_content": decoded_content}
    else:
        raise HTTPException(
            detail="Could not validate provided data. Either encoded_pass_key or pass_key are invalid!",
            status_code=status.HTTP_400_BAD_REQUEST
        )

# todo:
#  docker
#  testing
#  documentation enrichment
