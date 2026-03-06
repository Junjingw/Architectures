import pika
import os
import time
import json

# Configuración
rabbitmq_host = os.getenv('RABBITMQ_HOST', 'rabbitmq')
user = os.getenv('RABBITMQ_USER', 'user')
password = os.getenv('RABBITMQ_PASS', 'password')
credentials = pika.PlainCredentials(user, password)

# Conexión Robusta
connection = None
while connection is None:
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=rabbitmq_host, credentials=credentials)
        )
    except pika.exceptions.AMQPConnectionError:
        print(" [!] Catalog Service: RabbitMQ no listo. Reintentando...")
        time.sleep(3)

channel = connection.channel()
channel.exchange_declare(exchange='library_events', exchange_type='topic')

# Cola privada para el catálogo
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

# Suscribirse a préstamos aprobados
channel.queue_bind(exchange='library_events', queue=queue_name, routing_key='loan.approved')

def update_inventory(ch, method, props, body):
    data = json.loads(body)
    book_id = data.get('book_id')
    print(f" [Catalog] Libro {book_id} prestado. Actualizando stock en base de datos...")
    # Aquí iría la lógica de base de datos (SQL/NoSQL)
    
    # Opcional: Publicar evento de inventario actualizado
    ch.basic_publish(
        exchange='library_events', 
        routing_key='inventory.updated', 
        body=json.dumps({"book_id": book_id, "status": "out_of_stock"})
    )

channel.basic_consume(queue=queue_name, on_message_callback=update_inventory, auto_ack=True)
print(' [Catalog] Esperando confirmaciones de préstamo...')
channel.start_consuming()