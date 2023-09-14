from pydantic import BaseModel, Field


class SecretCreate(BaseModel):
    content: str = Field(min_length=1, title='Secret content. Should be longer than 1 symbol')
    pass_key: str = Field(min_length=5, title='Secret pass_key. Should be longer than 5 symbols.')
    pass_key_lifetime: str = Field('P1D', title="Lifetime of the secret")


class SecretBase(BaseModel):
    encoded_content: str = Field(..., title='Encoded content of the secret')
    encoded_pass_key: str = Field(..., title='Encoded pass key of the secret')
    pass_key_lifetime: str = Field(..., title="Lifetime of the secret")
    is_active: bool = Field(title="Secret activity status", default=True)
    link: str = Field(..., title="URL to access the secret")
