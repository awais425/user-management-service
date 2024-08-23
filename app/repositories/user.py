from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session

from app.db.model import UserORM
from app.schemas.user import UserCreate, UserUpdate


class UserRepository:
    def get_user_by_email(self, db: Session, email: str):
        try:
            return db.query(UserORM).filter(UserORM.email == email).first()
        except NoResultFound:
            raise HTTPException(status_code=404, detail="User not found")

    def get_user_by_id(self, db: Session, user_id: int):
        try:
            return db.query(UserORM).filter(UserORM.id == user_id).first()
        except NoResultFound:
            raise HTTPException(status_code=404, detail="User not found")

    def create_user(self, db: Session, user: UserCreate):
        try:
            db_user = UserORM(email=user.email, hashed_password=user.password)
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            return db_user
        except IntegrityError:
            raise HTTPException(status_code=400, detail="Email already exists")

    def update_user(self, db: Session, user_id: int, user_update: UserUpdate):
        db_user = self.get_user_by_id(db, user_id)
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        db_user.email = user_update.email
        db_user.is_active = user_update.is_active
        db.commit()
        db.refresh(db_user)
        return db_user

    def delete_user(self, db: Session, user_id: int):
        db_user = self.get_user_by_id(db, user_id)
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        db.delete(db_user)
        db.commit()
        return {"message": "User deleted successfully"}
