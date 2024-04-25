import pytest
import requests
from faker import Faker
from rest_framework import status
from testlib.client import AuthResponse, Client, RegisterResponse

fake = Faker()


def test_docs(client: Client) -> None:
    docs_response = requests.get(url=f"{client.host}/api/swagger/", timeout=5)
    assert docs_response.ok



def test_happy_auth(
    *,
    client: Client,
) -> None:

    email = fake.email()
    password = fake.password()
    registered = client.register(email=email, password=password)
    assert isinstance(registered, RegisterResponse)
    assert registered.message == f"{email} successfully registered"

    auth = client.authenticate(email=email, password=password)
    assert isinstance(auth, AuthResponse)
    assert auth.token
    assert auth.message == "User authenticated successfully"
