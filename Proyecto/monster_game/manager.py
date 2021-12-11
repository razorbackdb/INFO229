import mysql.connector
import os
import time
import pika
import create_database

print("start monster game...")
create_database.main()

DATABASE = "bot_game"

DATABASE_IP = str(os.environ['DATABASE_IP'])

DATABASE_USER = "root"
DATABASE_USER_PASSWORD = "root"
DATABASE_PORT = 3306

current_monster = None

time.sleep(10)

########### CONNEXIÓN A RABBIT MQ #######################

HOST = os.environ['RABBITMQ_HOST']
print("rabbit:" + HOST)

connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST))
channel = connection.channel()

# El consumidor utiliza el exchange 'cartero'
channel.exchange_declare(exchange='cartero',
                         exchange_type='topic',
                         durable=True)

# Se crea un cola temporaria exclusiva para este consumidor (búzon de correos)
result = channel.queue_declare(queue="monster_game",
                               exclusive=True,
                               durable=True)
queue_name = result.method.queue

# La cola se asigna a un 'exchange'
channel.queue_bind(exchange='cartero',
                   queue=queue_name,
                   routing_key="monster_game")

##########################################################

########## ESPERA Y HACE ALGO CUANDO RECIBE UN MENSAJE ####

print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(body.decode("UTF-8"))
    arguments = body.decode("UTF-8").split(" ")

    if (arguments[0] == "!monster"):
        db_connection = mysql.connector.connect(
            user=DATABASE_USER,
            host=DATABASE_IP,
            port=DATABASE_PORT,
            password=DATABASE_USER_PASSWORD)

        cursor = db_connection.cursor()
        cursor.execute(f"USE {DATABASE}")
        cursor.execute(
            f'''SELECT * FROM monsters WHERE selected=1;'''
        )

        monster = cursor.fetchone()

        if monster == None:
            cursor.execute(
                f'''SELECT name, emoji, atk, def, hp FROM monsters WHERE id_monster=1;'''
            )

            for (name, emoji, atk, def_, hp) in cursor:
                result = emoji
                print(result)

                ########## PUBLICA EL RESULTADO COMO EVENTO EN RABBITMQ ##########
                print("send a new message to rabbitmq: " + result)
                channel.basic_publish(exchange='cartero',
                                      routing_key="discord_writer",
                                      body=result)
                cursor.execute(
                    f'''UPDATE monsters SET selected=1 WHERE id_monster=1;'''
                )

                db_connection.commit()

        else:
            result = "Ya hay un monstruo. Haz algo!"
            print(result)

			########## PUBLICA EL RESULTADO COMO EVENTO EN RABBITMQ ##########
            print("send a new message to rabbitmq: " + result)
            channel.basic_publish(exchange='cartero',
									routing_key="discord_writer",
									body=result)


channel.basic_consume(queue=queue_name,
                      on_message_callback=callback,
                      auto_ack=True)

channel.start_consuming()

#######################
