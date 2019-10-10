from typing import Callable

import paho.mqtt.client as mqtt
import ssl
import json
import random

import time
from .models import Connection, Tag, TagLocation
from threading import Thread
from . import tags
from . import views


def on_connect(client, userdata, flags, rc):
    print(mqtt.connack_string(rc))


def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed to topic!")

class globalBS():
    sample_no = 0           # Comparison to rate, index is ++ for each packet
    sampling_rate = 0       # Limits the amount of logged entries
    start_time = 0          # Start time
    logging = False         # Logging Status
    loop_it = False         # Stops the logging if False
    mqtt_client = None      # Cloud client
    thread = None           # Thread with log entries, runs seperately
    sampling = None         # sampling_rate from DB
    active_tags = []        # active tagId's when running is started
    active_logged = False   # Is true if the activeted tags have been logged

def connect_cloud(on_message_handler: Callable, on_connect_handler: Callable=None,
                  on_subscribe_handler: Callable=None)-> mqtt.Client:

    connection_object = Connection.objects.get(connID=1)
    host = connection_object.host               # "mqtt.cloud.pozyxlabs.com"
    port = connection_object.port               # 443
    topic = connection_object.topic             # "5be2b12b7de46a38977805e0"
    username = connection_object.username       # "5be2b12b7de46a38977805e0"
    password = connection_object.password       # "53a04882-c773-4c13-ac18-b400a6d3ff03"
    sampling = connection_object.sampling

    mqtt_client = mqtt.Client(transport="websockets")

    mqtt_client.username_pw_set(username, password=password)

    mqtt_client.tls_set_context(context=ssl.create_default_context())

    mqtt_client.on_message = on_message_handler
    mqtt_client.on_connect = on_connect_handler if on_connect_handler is not None else on_connect
    mqtt_client.on_subscribe = on_subscribe_handler if on_subscribe_handler is not None else on_subscribe

    mqtt_client.connect(host, port=port)
    mqtt_client.subscribe(topic)

    return mqtt_client, sampling

def loop_run():
    while globalBS.loop_it:
        #print(globalBS.active_tags)
        globalBS.mqtt_client.loop()

def tear_down():
    globalBS.loop_it = False
    globalBS.logging = False
    # s = tags.print_tag_log(2)         # Writes tag#2 data from session to console


def initialize():
    globalBS.sample_no = 0

    globalBS.start_time = time.time()
    globalBS.logging = True

    globalBS.mqtt_client, globalBS.sampling_rate = connect_cloud(on_message_cloud_1)

    globalBS.loop_it = True

    globalBS.thread = Thread(target = loop_run)
    globalBS.thread.start()
    globalBS.views = views.globalViews()

def on_message_cloud(client, userdata, msg):
    #print("sample_no = " + str(self.sample_no))
    #print("Går vi inn?")
    if not globalBS.logging or globalBS.sample_no < globalBS.sampling_rate:
        globalBS.sample_no += 1
        return
    try:
        globalBS.sample_no = 1
        tags_data_json = msg.payload.decode()
        tags_data = json.loads(tags_data_json)
        # if (self.iterate):                      # Prints one data-packet
        #     print(tags_data)
        #     self.iterate = False
        #print("New print!!" + "\n" + str(tags_data))  # --> Contains the json data!!!
        cn = 1
        print("GÅR INNI HER ------------------------------------------------")
        for tag_data in tags_data:                      # For each tag in the message
            tag_time = float(tag_data["timestamp"])
            tag_ID = int(tag_data["tagId"])
            if not globalBS.active_logged:
                globalBS.active_tags.append(tag_ID)
                if not Tag.objects.filter(tagID=tag_ID).exists():
                    new_tag = Tag.objects.create(tagID=tag_ID, name="Tag#" + str(tag_ID))

                    new_tag.save()
                    print("NEW TAG CREATED!")
                if cn == len(tags_data):
                    globalBS.active_logged = True
                else:
                    cn += 1
            try:
                x = tag_data["data"]["coordinates"]["x"]
                y = tag_data["data"]["coordinates"]["y"]
                #z = tag_data["data"]["coordinates"]["z"]

                vx = tag_data["data"]["velocity"]["x"]
                vy = tag_data["data"]["velocity"]["y"]

                tag_time = tag_time - globalBS.start_time

                if (tag_time < 0):
                    break

                if not globalBS.active_logged:
                    pass
                else:
                    if tag_ID in globalBS.active_tags:
                        current_tag = Tag.objects.get(tagID=tag_ID)
                        new_tag_read = TagLocation.objects.create(tagID=current_tag, timestamp=tag_time, x_pos=x,
                            y_pos=y, vx=vx, vy=vy)
                        new_tag_read.save()


                #vz = tag_data["data"]["velocity"]["z"]

                #blink = tag_data["data"]["tagData"]["blinkIndex"]

                # if time() - tag_time <= 1:
                #     if (tag_ID == "7"):
                #         tag_time = tag_time - globalBS.start_time
                #         s = "{},{},{},{},{},{},{}\n".format(tag_time, tag_ID, x, y, vx, vy)
                #         #print(s)
                #         #print("WRITING")
            except:
                # this will occur when there is no valid coordinates
                pass

    except Exception as e:
        print("No valid tag data: {}".format(e))

def on_message_cloud_1(client, userdata, msg):
    if not globalBS.logging or globalBS.sample_no < globalBS.sampling_rate:
        globalBS.sample_no += 1
        return
    try:
        globalBS.sample_no = 1
        tags_data_json = msg.payload.decode()
        tags_data = json.loads(tags_data_json)
        arr = []
        for tag_data in tags_data:                      # For each tag in the message
            tag_time = float(tag_data["timestamp"])
            tag_ID = int(tag_data["tagId"])
            try:
                x = tag_data["data"]["coordinates"]["x"]
                y = tag_data["data"]["coordinates"]["y"]
                vx = tag_data["data"]["velocity"]["x"]
                vy = tag_data["data"]["velocity"]["y"]
                tag_time = tag_time - globalBS.start_time

                if (tag_time < 0):
                    break
                print(str(tag_ID))
                arr.append([tag_ID, tag_time, x, y, vx, vy])
                views.incremenet_log_count()

                # if not globalBS.active_logged:
                #     print("Skjer ikke")
                #     pass
                # else:
                #     # Data to send to view.py when requested
                #     s = [tag_ID, tag_time, x, y, vx, vy]
                #     print("TOMT?")
                #     globalBS.views.current_stack.append([tag_ID, tag_time, x, y, vx, vy])
            except:
                # this will occur when there is no valid coordinates
                pass
        views.sent_data(arr)
        #print(globalBS.views.current_stack)
    except Exception as e:
        print("No valid tag data: {}".format(e))


# def find_active_tags(tags_data):
#     active_tags = []
#     for tag in tags_data:
#         active_tags.append(tag["tagId"])
#     return active_tags

# class Session():
#     def __init__(self, sampling_rate):
#         super().__init__()
#
#         stop_thread = False
#
#         self.sample_no = 0
#         self.sampling_rate = sampling_rate
#
#         print("SamplingRate = " + str(sampling_rate))
#
#         self.start_time = 0
#
#         self.logging = True
#
#         self.mqtt_client = connect_cloud(self.on_message_cloud)
#
#         self.loop_it = True
#
#         self.thread = Thread(target = loop_run, args = (self.loop_it, self.mqtt_client, self.sample_no, ))
#
#         self.thread.start()
#
#
#
#     # callback triggered by a new Pozyx data packet
#     def on_message_cloud(self, client, userdata, msg):
#         #print("sample_no = " + str(self.sample_no))
#         if not self.logging or self.sample_no < self.sampling_rate:
#             self.sample_no += 1
#             return
#         try:
#             self.sample_no = 1
#             tags_data_json = msg.payload.decode()
#             tags_data = json.loads(tags_data_json)
#             # if (self.iterate):                      # Prints one data-packet
#             #     print(tags_data)
#             #     self.iterate = False
#             #print(tags_data)  # --> Contains the json data!!!
#
#             self.active = find_active_tags(tags_data)
#
#             for tag_data in tags_data:                      # For each tag in the message
#                 tag_time = float(tag_data["timestamp"])
#                 tag_ID = tag_data["tagId"]
#                 try:
#                     x = tag_data["data"]["coordinates"]["x"]
#                     y = tag_data["data"]["coordinates"]["y"]
#                     #z = tag_data["data"]["coordinates"]["z"]
#
#                     vx = tag_data["data"]["velocity"]["x"]
#                     vy = tag_data["data"]["velocity"]["y"]
#                     #vz = tag_data["data"]["velocity"]["z"]
#
#                     blink = tag_data["data"]["tagData"]["blinkIndex"]
#
#                     if time() - tag_time <= 1:
#                         if (tag_ID == "7"):
#                             tag_time = tag_time - self.start_time
#                             s = "{},{},{},{},{},{},{}\n".format(tag_time, tag_ID, x, y, vx, vy, blink)
#                             #print(s)
#                             #print("WRITING")
#                 except:
#                     # this will occur when there is no valid coordinates
#                     pass
#
#         except Exception as e:
#             print("No valid tag data: {}".format(e))





# def main(sampling_rate, run):
#     if run:
#         print("Starting loop")
#         app = Session(sampling_rate)
#     else:
#         print("CLICK!!")
#         app.kill()
#
#
# if __name__ == '__main__':
#     main()
