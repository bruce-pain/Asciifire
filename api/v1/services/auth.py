from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from api.utils import password_utils
from api.core import response_messages
from api.v1.schemas import auth as auth_schema
from api.v1.models.user import User


def register(db: Session, schema: auth_schema.RegisterRequest) -> User:
    """Creates a new user

    Args:
        db (Session): Database Session
        schema (auth_schema.RegisterRequest): Registration schema

    Returns:
        User: User object for the newly created user
    """

    # check if user with username already exists
    if db.query(User).filter(User.username == schema.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username already exists",
        )

    # Hash password
    password_hash = password_utils.hash_password(password=schema.password)

    user = User(username=schema.username, password_hash=password_hash)

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def authenticate(db: Session, schema: auth_schema.LoginRequest) -> User:
    """Authenticates a registered user

    Args:
        db (Session): Database Session
        schema (auth_schema.LoginRequest): Login Request schema

    Returns:
        User: Authenticated user
    """

    # check if user with the username exists
    user = db.query(User).filter(User.username == schema.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="invalid username",
        )

    if not password_utils.verify_password(schema.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=response_messages.INVALID_PASSWORD,
        )

    return user
