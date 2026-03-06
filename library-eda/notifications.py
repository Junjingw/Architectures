import pika, os, time

time.sleep(15)
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=os.getenv('RABBITMQ_HOST'),
    credentials=pika.PlainCredentials(os.getenv('RABBITMQ_USER'), os.getenv('RABBITMQ_PASS'))
))
channel = connection.channel()
channel.exchange_declare(exchange='library_events', exchange_type='topic')

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

# Bind to ALL events
channel.queue_bind(exchange='library_events', queue=queue_name, routing_key='#')

def callback(ch, method, props, body):
    print(f" [NOTIFICATION] Event Detected: {method.routing_key} | Data: {body.decode()}")

channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
print(' [Notifications] Logging all system activity...')
channel.start_consuming()

