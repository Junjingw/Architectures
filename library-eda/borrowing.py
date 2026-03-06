import pika, os, time, json

time.sleep(15)
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=os.getenv('RABBITMQ_HOST'),
    credentials=pika.PlainCredentials(os.getenv('RABBITMQ_USER'), os.getenv('RABBITMQ_PASS'))
))
channel = connection.channel()
channel.exchange_declare(exchange='library_events', exchange_type='topic')

# Create a private queue for this service
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

# Bind to loan requests
channel.queue_bind(exchange='library_events', queue=queue_name, routing_key='loan.requested')

def on_request(ch, method, props, body):
    data = json.loads(body)
    print(f" [Borrowing] Processing loan for book {data['book_id']}...")
    time.sleep(2) # Simulate logic
    
    # Publish success event
    ch.basic_publish(exchange='library_events', routing_key='loan.approved', body=json.dumps(data))
    print(f" [Borrowing] Published: loan.approved")

channel.basic_consume(queue=queue_name, on_message_callback=on_request, auto_ack=True)
print(' [Borrowing] Waiting for loan requests...')
channel.start_consuming()

