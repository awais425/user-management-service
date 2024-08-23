# app/mappers/user_mapper.py


from app.core.model import User as UserModel
from app.repositories.user import UserORM
from app.schemas.user import User, UserCreate, UserUpdate


def orm_to_model(orm_user: UserORM) -> UserModel:
    return UserModel(
        id=orm_user.id,
        email=orm_user.email,
        hashed_password=orm_user.hashed_password,
        is_active=orm_user.is_active,
    )


def model_to_schema(user_model: UserModel) -> User:
    return User(
        id=user_model.id, email=user_model.email, is_active=user_model.is_active
    )


def create_schema_to_model(user_create: UserCreate) -> UserModel:
    return UserModel(
        # type: ignore
        email=user_create.email,
        hashed_password=user_create.password,
        is_active=user_create.is_active,
    )


def update_schema_to_model(user_update: UserUpdate, user_model: UserModel) -> UserModel:
    user_model.email = user_update.email
    user_model.is_active = user_update.is_active
    return user_model
