# tests/test_producer.py
import unittest
from unittest.mock import patch, MagicMock
from app.services.producer_service import KafkaProducerService

class TestKafkaProducerService(unittest.TestCase):
    @patch('app.services.producer_service.KafkaProducer')
    def setUp(self, mock_kafka_producer):
        self.mock_producer_instance = MagicMock()
        mock_kafka_producer.return_value = self.mock_producer_instance
        self.kafka_producer_service = KafkaProducerService(
            KAFKA_SERVER="192.168.49.2:30092", KAFKA_TOPIC="my-topic"
        )

    def test_send_message(self):
        message = {'event': 'UserCreated', 'user_id': 1, 'email': 'user@example.com', 'is_active': True}
        self.kafka_producer_service.send(message)
        self.mock_producer_instance.send.assert_called_once_with('my-topic', message)
        self.mock_producer_instance.flush.assert_called_once()

if __name__ == '__main__':
    unittest.main()
