from pydantic import BaseModel, Field

from app.models.enums import PassKeyLifetimeEnum


class SecretCreate(BaseModel):
    content: str = Field(
        min_length=1, title='Secret content. Should be longer than 1 symbol', example='Your secret content'
    )
    pass_key: str = Field(
        min_length=5, title='Secret pass_key. Should be longer than 5 symbols.', example="Your secret pass_key"
    )


class SecretBase(BaseModel):
    encoded_content: str = Field(..., title='Encoded content of the secret')
    encoded_pass_key: str = Field(..., title='Encoded pass key of the secret')
    pass_key_lifetime: PassKeyLifetimeEnum = Field(PassKeyLifetimeEnum.one_day, title="Lifetime of the secret")
    is_active: bool = Field(title="Secret activity status", default=True)
    link: str = Field(..., title="URL to access the secret")
