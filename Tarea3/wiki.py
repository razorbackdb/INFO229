#!/usr/bin/env python
import pika
import sys
import pageviewapi.period
import wikipedia

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

#Creamos el exchange 'logs' de tipo 'fanout'
channel.exchange_declare(exchange='content', exchange_type='fanout')

channel.exchange_declare(exchange='views', exchange_type='fanout')

article = u' '.join(sys.argv[1:]) or u'Valdivia'

content_message = str(pageviewapi.period.sum_last('en.wikipedia', article, last=365,
                            access='all-access', agent='all-agents'))

views_message = str(wikipedia.page(article).content)

#Publicamos los mensajes a través del exchange 'logs' 
channel.basic_publish(exchange='content', routing_key='', body=content_message)
channel.basic_publish(exchange='views', routing_key='', body=views_message)

print(" [x] Sent %r" % content_message)
print(" [x] Sent %r" % views_message)
connection.close()
