from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.services.producer_service import KafkaProducerService
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserUpdate
# from app.services.kafka_service import KafkaService

class UserService:
    def __init__(self, user_repository: UserRepository, kafka_producer:KafkaProducerService):
        self.user_repository = user_repository
        self.kafka_producer = kafka_producer
    

    def create_user(self, db: Session, user: UserCreate):
        user = self.user_repository.create_user(db, user)
        if not user:
            raise HTTPException(status_code=404, detail="User not created")
        
        # Send message to Kafka
        self.kafka_producer.send({
            "event": "UserCreated",
            "user_id": user.id,
            "email": user.email,
            "is_active": user.is_active,
        })
        return user
# class UserService:
#     def __init__(self, user_repository: UserRepository, kafka_service: KafkaService):
#         self.user_repository = user_repository
#         self.kafka_service = kafka_service

#     def create_user(self, db: Session, user: UserCreate):
#         user = self.user_repository.create_user(db, user)
#         if not user:
#             raise HTTPException(status_code=404, detail="User not created")
        
#         # Produce message to Kafka
#         self.kafka_service.produce_message(key=str(user.id), value="User created: {}".format(user.email))
#         return user
    def get_user_by_email(self, db: Session, email: str):
        user = self.user_repository.get_user_by_email(db, email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def get_user_by_id(self, db: Session, user_id: int):
        user = self.user_repository.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def update_user(self, db: Session, user_id: int, user_update: UserUpdate):
        user = self.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return self.user_repository.update_user(db, user_id, user_update)

    def delete_user(self, db: Session, user_id: int):
        user = self.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return self.user_repository.delete_user(db, user_id)
