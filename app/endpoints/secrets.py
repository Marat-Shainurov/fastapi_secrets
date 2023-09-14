from bson import ObjectId
from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from starlette import status

from app.database.config import db
from app.models.secrets import SecretBase, SecretCreate
from app.schemas.serializers import serializerDict
from app.services.encode_services import decode_data
from app.services.secrets_services import create_secret_model

secrets = APIRouter()


@secrets.post("/secrets/generate", response_model=SecretBase, status_code=status.HTTP_201_CREATED)
async def create_secret(secret: SecretCreate):
    new_secret = create_secret_model(secret)
    result = db.local.secrets.insert_one(dict(new_secret))
    created_secret = db.local.secrets.find_one({"_id": ObjectId(result.inserted_id)})
    created_secret_dict = serializerDict(created_secret)
    return created_secret_dict


@secrets.get("/secrets/read/{encoded_pass_key}")
async def read_secret(encoded_pass_key: str, pass_key: str):
    secret = db.local.secrets.find_one({"encoded_pass_key": encoded_pass_key})
    decoded_pass_key = decode_data(encoded_pass_key, secret_encode_key=pass_key)
    if secret and decoded_pass_key == pass_key:
        if secret.get("is_active") is False:
            raise HTTPException(
                detail="The secret has been read already!",
                status_code=status.HTTP_403_FORBIDDEN
            )
        else:
            decoded_content = decode_data(dict(secret).get("encoded_content"), secret_encode_key=pass_key)
            db.local.secrets.find_one_and_update({"_id": ObjectId(secret.get("_id"))}, {"$set": {"is_active": False}})
            return {"secret_content": decoded_content}
    else:
        raise HTTPException(
            detail="Could not validate provided data",
            status_code=status.HTTP_400_BAD_REQUEST
        )

# todo:
#  docker
#  testing
#  documentation enrichment
