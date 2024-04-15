import bcrypt
import prisma
import prisma.models
from pydantic import BaseModel


class CreateUserResponse(BaseModel):
    """
    A confirmation of successful user registration, including the unique identifier and email of the new account without exposing the password.
    """

    user_id: str
    email: str
    message: str


async def create_user(email: str, password: str) -> CreateUserResponse:
    """
    Registers a new user with email and password.

    This function takes an email and password as input and attempts to create a new user in the database.
    The password is hashed for security before it is stored. It checks if the email is unique and if so, creates the user.

    Args:
        email (str): The email address for the new user account. It must be unique across the system.
        password (str): The password for the new user account. This will be hashed before storage for security purposes.

    Returns:
        CreateUserResponse: A confirmation of successful user registration, including the unique identifier
                            and email of the new account without exposing the password.

    Example:
        create_user("newuser@example.com", "password123")
        > CreateUserResponse(user_id="some-unique-uuid", email="newuser@example.com", message="User successfully created.")
    """
    existing_user = await prisma.models.User.prisma().find_unique(
        where={"email": email}
    )
    if existing_user:
        return CreateUserResponse(
            user_id="",
            email="",
            message="Email already exists. Please choose a different email.",
        )
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode(
        "utf-8"
    )
    new_user = await prisma.models.User.prisma().create(
        data={"email": email, "password": hashed_password}
    )
    return CreateUserResponse(
        user_id=new_user.id, email=new_user.email, message="User successfully created."
    )
