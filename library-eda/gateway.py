import pika, os, time, json

time.sleep(15) # Wait for RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=os.getenv('RABBITMQ_HOST'),
    credentials=pika.PlainCredentials(os.getenv('RABBITMQ_USER'), os.getenv('RABBITMQ_PASS'))
))
channel = connection.channel()

# Define the Topic Exchange
channel.exchange_declare(exchange='library_events', exchange_type='topic')

print(" [API Gateway] Ready to send requests...")
while True:
    event_data = {"book_id": 101, "user_id": "user_01", "timestamp": time.time()}
    message = json.dumps(event_data)
    
    # Routing Key: loan.requested
    channel.basic_publish(exchange='library_events', routing_key='loan.requested', body=message)
    print(f" [Gateway] Sent: Loan Requested for Book {event_data['book_id']}")
    
    time.sleep(10)

