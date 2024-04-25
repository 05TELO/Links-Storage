from dataclasses import dataclass
import logging
from typing import final

import orjson
import requests
from pydantic import BaseModel
from pydantic import ConfigDict


class MyModel(BaseModel):
    class Meta:
        model_config = ConfigDict(extra='forbid')
        json_dumps = orjson.dumps
        json_loads = orjson.loads
        orm_mode = True
        validate_assignment = True

class RegisterResponse(MyModel):
    message: str

class AuthResponse(MyModel):
    message: str
    token: str

@final
@dataclass
class Client:
    host: str
    session: requests.Session

    class ApiError(RuntimeError):
        def __init__(
            self,
            *args: tuple,
            message: str,
            http_code: int,
        ):
            super().__init__(*args)
            self.message = message
            self.http_code = http_code

        def __str__(self) -> str:
            return f"message:{self.message}, http_code:{self.http_code}"

    def register(
        self,
        *,
        email: str,
        password: str,
    ) -> RegisterResponse:
        response = self.session.post(
            f"{self.host}/api/register/",
            data=orjson.dumps(
                {
                    "email": email,
                    "password": password,
                }
            ),
        )

        assert response.ok, response.text
        payload = RegisterResponse.model_validate_json(response.text)
        return payload


    def authenticate(
        self,
        *,
        email: str,
        password: str,
    ) -> AuthResponse:
        response = self.session.post(
            f"{self.host}/api/login/",
            data=orjson.dumps({
                "email": email,
                "password": password,
                }
            ),

        )

        assert response.ok, response.text
        payload = AuthResponse.model_validate_json(response.text)
        return payload
