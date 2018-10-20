'''
Written by Debojit Kaushik  (Timestamp)
'''
import os
import sys
import traceback
import pika
import json

from flow import Speech2TextRequest, Text2CodeRequest, HEADERS, PARAMS
from actions import Action

class MessageBroker:
    @staticmethod
    def send_message(queue_ID, json_data={"Message": None}):
        """Method to send/publish messages on the queue."""
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
            channel = connection.channel()
            channel.queue_declare(queue_ID)
            channel.basic_publish(body = json.dumps(json_data), routing_key=queue_ID, exchange = "")
            connection.close()
        except Exception:
            print(traceback.format_exc())

    @staticmethod
    def receive_callback(ch, method, properties, body):
        try:
            print("Recieved a message.")
            #Need to initialise Python engine. 
            action_dic = json.loads(body)
            if action_dic["action"] == "init":
                MessageBroker.send_message("py_to_ele", json_data = json.dumps({'status': 'listening'}))
                #INSERT AMLAANS FUNCTION CALL.
                res = Text2CodeRequest._create_to_code_request("create a variable called X Y and Z", HEADERS, PARAMS)
                action_data = Action.get_action(res)
                print(action_data)
                MessageBroker.send_message("py_to_ele", json.dumps(action_data))
        except Exception:
            print(traceback.format_exc())
            
    @staticmethod
    def receive_message(queue_ID):
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
            channel = connection.channel()
            channel.queue_declare(queue_ID)
            channel.basic_consume(MessageBroker.receive_callback, queue = queue_ID, no_ack = True)
            print("Starting to listen...")
            channel.start_consuming()
        except Exception:
            print(traceback.format_exc())


if __name__ == '__main__':
    try:
        # print("Hey")
        # message = {"first_name": "Debojit", "last_name": "Kaushik", "Age": 27}
        # MessageBroker.send_message("py_to_js", json_data = json.dumps(message))
        MessageBroker.receive_message("ele_to_py")
    except Exception:
        print(traceback.format_exc())