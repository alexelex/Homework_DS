import smtplib
import pika
import json
from config import SERVER, LOGIN

def callback(ch, method, _, data):
    try:
        body = json.loads(data)
        server = smtplib.SMTP(SERVER["host"], SERVER["port"])
        server.starttls()
        server.login(LOGIN["email"], LOGIN["password"])
        server.sendmail(LOGIN["email"], body["recipient"], body["text"])
        server.close()
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except smtplib.SMTPException:
        pass


conn = pika.BlockingConnection(pika.ConnectionParameters("mq", 5672, "/", pika.PlainCredentials("user", "user")))
chan = conn.channel()
chan.queue_declare(queue="main")
chan.basic_consume(queue="main", on_message_callback=callback)
chan.start_consuming()
