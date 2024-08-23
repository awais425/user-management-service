# # tests/test_consumer.py
# import unittest
# from unittest.mock import patch, Mock
# from app.services.consumer_service import KafkaConsumerService

# class TestKafkaConsumerService(unittest.TestCase):
#     def setUp(self):
#         self.kafka_consumer_service = KafkaConsumerService(KAFKA_SERVER="192.168.49.2:30092", KAFKA_TOPIC="my-topic")

#     @patch('kafka.KafkaConsumer')
#     def test_consume_message(self, mock_kafka_consumer):
#         message = {'event': 'UserCreated', 'user_id': 1, 'email': 'user@example.com', 'is_active': True}
#         mock_consumer = mock_kafka_consumer.return_value
#         mock_consumer.poll.return_value = {0: [Mock(value=message)]}
#         self.kafka_consumer_service.consumer = mock_consumer  # Set the consumer attribute to the mocked KafkaConsumer object
#         self.kafka_consumer_service.consume()
#         # Verify that the message is consumed successfully
#         # ...

# if __name__ == '__main__':
#     unittest.main()

# tests/test_consumer.py
import unittest
from unittest.mock import patch, MagicMock
from app.services.consumer_service import KafkaConsumerService
from app.schemas.user import UserCreate

class TestKafkaConsumerService(unittest.TestCase):
    @patch('app.services.consumer_service.KafkaConsumer')
    @patch('app.services.consumer_service.UserRepository')
    def setUp(self, mock_user_repository, mock_kafka_consumer):
        self.mock_consumer_instance = MagicMock()
        self.mock_user_repository_instance = MagicMock()
        
        mock_kafka_consumer.return_value = self.mock_consumer_instance
        mock_user_repository.return_value = self.mock_user_repository_instance
        
        self.kafka_consumer_service = KafkaConsumerService(
            KAFKA_SERVER="192.168.49.2:30092", KAFKA_TOPIC="my-topic"
        )

    def test_consume_message(self):
        # Define the message to be consumed
        message = {
            'event': 'UserCreated',
            'email': 'user@example.com',
            'is_active': True
        }
        # Mock Kafka message
        mock_message = MagicMock()
        mock_message.value = message

        # Configure the consumer to return the mock message
        self.mock_consumer_instance.__iter__.return_value = iter([mock_message])

        # Call the consume method
        self.kafka_consumer_service.consume()

        # Verify that the UserRepository's create_user method was called with correct arguments
        self.mock_user_repository_instance.create_user.assert_called_once_with(
            unittest.mock.ANY,  # For the SessionLocal object
            UserCreate(
                email='user@example.com',
                password='password',  # Since password is hardcoded in your consumer code
                is_active=True
            )
        )

if __name__ == '__main__':
    unittest.main()
