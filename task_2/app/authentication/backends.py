from typing import Any
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.base_user import AbstractBaseUser
from django.http import HttpRequest

class EmailAuth(BaseBackend):
    def authenticate(self, request: HttpRequest, email: str, password:str ) -> AbstractBaseUser | None:
        return super().authenticate(request, username=email, password=password)
    def get_user(self, user_id: int) -> AbstractBaseUser | None:
        return super().get_user(user_id)