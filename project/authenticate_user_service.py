from datetime import datetime, timedelta

import prisma
import prisma.models
from bcrypt import checkpw
from jose import jwt
from pydantic import BaseModel


class AuthenticateUserResponse(BaseModel):
    """
    Response model for user authentication. Returns an access token on successful authentication.
    """

    access_token: str
    token_type: str
    expires_in: int


SECRET_KEY = "YOUR_SECRET_KEY_HERE"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30


async def authenticate_user(email: str, password: str) -> AuthenticateUserResponse:
    """
    Authenticates a user and returns an access token.

    This function finds a user by their email, verifies the provided password against the hashed
    password stored in the database, and generates a JWT access token if authentication is successful.

    Args:
        email (str): The user's email address as registered.
        password (str): The user's password.

    Returns:
        AuthenticateUserResponse: Response model for user authentication, including the access token on successful authentication.
    """
    user = await prisma.models.User.prisma().find_unique(where={"email": email})
    if user and checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        token = create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        return AuthenticateUserResponse(
            access_token=token,
            token_type="bearer",
            expires_in=int(access_token_expires.total_seconds()),
        )
    else:
        fake_response_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        return AuthenticateUserResponse(
            access_token="invalid",
            token_type="bearer",
            expires_in=int(fake_response_expires.total_seconds()),
        )


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    Utility function for creating JWT access tokens.

    Args:
        data (dict): Data payload to encode in the JWT token.
        expires_delta (timedelta, optional): Expiration time for the token. Defaults to None.

    Returns:
        str: Encoded JWT token as a string.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
