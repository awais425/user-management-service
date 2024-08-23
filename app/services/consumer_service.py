# app/services/consumer_service.py
from kafka import KafkaConsumer
from app.db.session import SessionLocal
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate
import threading

class KafkaConsumerService:
    def __init__(self, KAFKA_SERVER: str, KAFKA_TOPIC: str):
        self.consumer = KafkaConsumer(
            KAFKA_TOPIC,
            bootstrap_servers=KAFKA_SERVER,
            group_id='user-management-group',
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            auto_commit_interval_ms=1000
        )
        self.user_repository = UserRepository()

    def consume(self):
        for message in self.consumer:
            try:
                event = message.value
                if event['event'] == 'UserCreated':
                    user_create = UserCreate(
                        email=event['email'],
                        password='password',  # todo: handle password hashing
                        is_active=event['is_active']
                    )
                    self.user_repository.create_user(SessionLocal(), user_create)
                    print(f"Created user with email {event['email']}")
                else:
                    print(f"Unknown event type: {event['event']}")
            except Exception as e:
                print(f"Error consuming message: {e}")

    def start_consumer(self):
        threading.Thread(target=self.consume).start()