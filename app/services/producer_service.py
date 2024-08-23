from kafka import KafkaProducer
import json

class KafkaProducerService:
    def __init__(self, KAFKA_SERVER: str, KAFKA_TOPIC: str):
        self.producer = KafkaProducer(
            bootstrap_servers=KAFKA_SERVER,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        self.KAFKA_TOPIC = KAFKA_TOPIC

    def send(self, message: dict):
        try:
            self.producer.send(self.KAFKA_TOPIC, message)
            self.producer.flush()
        except Exception as e:
            print(f"Failed to send message to Kafka: {e}")

# from kafka import KafkaProducer, KafkaConsumer
# from kafka.errors import KafkaError, NoBrokersAvailable

# class KafkaService:
#     def __init__(self, broker_url: str, topic: str):
#         try:
#             self.producer = KafkaProducer(bootstrap_servers=broker_url)
#             self.consumer = KafkaConsumer(
#                 topic,
#                 bootstrap_servers=broker_url,
#                 group_id='user-management-group',
#                 auto_offset_reset='earliest'
#             )
#         except NoBrokersAvailable as e:
#             print(f"Error: No brokers available at {broker_url}.")
#             raise e

#         self.topic = topic

#     def produce_message(self, key: str, value: str):
#         try:
#             # Send message and use the callback for delivery report
#             future = self.producer.send(self.topic, key=key.encode('utf-8'), value=value.encode('utf-8'))
#             future.add_callback(self.delivery_report)
#             future.add_errback(self.delivery_error)
#             self.producer.flush()  # Ensure all buffered records are sent
#         except KafkaError as e:
#             print(f"Failed to send message: {e}")
#             raise e

#     def consume_messages(self):
#         try:
#             for message in self.consumer:
#                 print(f'Received message: {message.value.decode("utf-8")}')
#         except KafkaError as e:
#             print(f"Error while consuming messages: {e}")
#             raise e

#     @staticmethod
#     def delivery_report(record_metadata):
#         print('Message delivered to {} [{}]'.format(record_metadata.topic, record_metadata.partition))

#     @staticmethod
#     def delivery_error(excp):
#         print(f"Message delivery failed: {excp}")
