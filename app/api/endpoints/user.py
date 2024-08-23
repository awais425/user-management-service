from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.repositories.user import UserRepository
from app.schemas.user import User, UserCreate, UserUpdate
from app.services.user_service import UserService
from app.services.consumer_service import KafkaConsumerService
from app.services.producer_service import KafkaProducerService
# from app.services.kafka_service import KafkaService

def get_kafka_producer_service():
    return KafkaProducerService(
        KAFKA_SERVER="192.168.49.2:30092",  
        KAFKA_TOPIC="my-topic"
    )

# import os
# from dotenv import load_dotenv
# load_dotenv()
# def get_kafka_producer_service():
#     broker_url = os.getenv("KAFKA_BROKER_URL", "kafka:9092")  # Default to "kafka:9092"
#     topic = os.getenv("KAFKA_TOPIC", "my-topic")  
#     return KafkaProducerService(broker_url=broker_url, topic=topic)
router = APIRouter()
user_repository = UserRepository()
Kafka_producer  = get_kafka_producer_service()
user_service = UserService(user_repository,Kafka_producer)
kafka_consumer_service = KafkaConsumerService(KAFKA_SERVER="192.168.49.2:30092", KAFKA_TOPIC="my-topic")
kafka_consumer_service.start_consumer()

@router.post("/users/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    return user_service.create_user(db=db, user=user)


@router.get("/users/email/{email}", response_model=User)
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    return user_service.get_user_by_email(db=db, email=email)


@router.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    return user_service.update_user(db=db, user_id=user_id, user_update=user_update)


@router.delete("/users/{user_id}", response_model=dict)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return user_service.delete_user(db=db, user_id=user_id)
