from typing import Iterable
import pytest
import requests
from testlib.client import Client

default_headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "User-Agent": "Penetrator/9000",
}


@pytest.fixture(scope="session")
def client() -> Iterable[Client]:
    with requests.Session() as session:
        session.headers.update(default_headers)
        yield Client(host="http://localhost:8000", session=session)