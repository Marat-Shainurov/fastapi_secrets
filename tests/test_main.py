import time

from fastapi.testclient import TestClient

from app.models.secrets import SecretCreate
from app.services.encode_services import decode_data
from main import app
from fastapi import status

client = TestClient(app)


def test_create_secret():
    new_secret = SecretCreate(content="Hello, dear friend!", pass_key="hello_key")
    response = client.post("/secrets/generate?pass_key_lifetime=PT1M", json=new_secret.model_dump())
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["pass_key_lifetime"] == "PT1M"
    assert response.json()["is_active"] is True
    assert response.json()["link"][:35] == "http://127.0.0.1:8000/secrets/read/"
    assert decode_data(response.json()["encoded_pass_key"], 'hello_key') == 'hello_key'
    assert decode_data(response.json()["encoded_content"], 'hello_key') == 'Hello, dear friend!'


def test_read_secret():
    new_secret = SecretCreate(content="Hey! Here is a top-secret message", pass_key="top_secret_key")
    response_post = client.post("/secrets/generate?pass_key_lifetime=PT1M", json=new_secret.model_dump())
    response_get = client.get(f"/secrets/read/{response_post.json()['encoded_pass_key']}?pass_key=top_secret_key")
    assert response_get.status_code == status.HTTP_200_OK
    assert response_get.json() == {"secret_content": "Hey! Here is a top-secret message"}
    response_get_again = client.get(f"/secrets/read/{response_post.json()['encoded_pass_key']}?pass_key=top_secret_key")
    assert response_get_again.json()["detail"] == "The secret has been read already!"


def test_read_expired_key():
    new_secret = SecretCreate(
        content="Hey! Here is a top-secret message. Read it ASAP!", pass_key="top_secret_key"
    )
    response_post = client.post("/secrets/generate?pass_key_lifetime=PT1M", json=new_secret.model_dump())
    time.sleep(70)
    response_get = client.get(f"/secrets/read/{response_post.json()['encoded_pass_key']}?pass_key=top_secret_key")
    assert response_get.status_code == status.HTTP_403_FORBIDDEN
    assert response_get.json()["detail"] == "Your pass key has expired!"


def test_read_secret_invalid_input():
    new_secret = SecretCreate(content="Hey! Here is a top-secret message", pass_key="top_secret_key")
    response_post = client.post("/secrets/generate?pass_key_lifetime=PT1M", json=new_secret.model_dump())
    response_bad_key = client.get(f"/secrets/read/{response_post.json()['encoded_pass_key']}?pass_key=invalid_key")
    assert response_bad_key.status_code == status.HTTP_400_BAD_REQUEST
    assert response_bad_key.json()["detail"] == "Either encoded_pass_key or pass_key are invalid!"
    response_bad_url = client.get(f"/secrets/read/invalid-path-encoded-key-in-url?pass_key=top_secret_key")
    assert response_bad_url.status_code == status.HTTP_400_BAD_REQUEST
    assert response_bad_url.json()["detail"] == "Either encoded_pass_key or pass_key are invalid!"
