from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, Group
from .models import Room, Zone, Obstruction, Tag, Connection, Session, TagLocation
from django.contrib.auth import logout
from .forms import *
from datetime import datetime, timedelta
from . import connect

# def view_dash(request):
#     # if not request.user.is_authenticated:
#     #     return redirect('/')
#     antall = Tag.objects.count()
#     if antall is None:
#         antall = 0
#     status = False
#     print("ANTALL!!! ======== " + str(antall))
#
#     return render(request, "dashboard.html", {'active': antall, 'status': status})

class globalViews():
    vars = None
    connection = None
    file_path = None
    received_stack = []
    times_logged = 0

    active_session = False
    session_name = None
    session_ID = None

# This connects to the server
def connect_to():
    print("CONNECT_TO")

    globalViews.vars = connect.globalBS()
    print(globalViews.vars.sample_no)

    connection = connect.initialize()

    print("SAMPPLING RATE = " + str(globalViews.vars.sampling_rate))

    status = globalViews.vars.logging

    #print(str(client))
    #return render(request, "dashboard.html", {'status': status})
    #return render(request, "dashboard.html", {'status': status})

def disconnect(request):
    print("CLIKKEt paa denne")
    connect.tear_down()
    status = False
    return render(request, "dashboard.html", {'status': status})

def home(request):
    status = Connection.objects.get(connID=1).connected
    return render(request, "dashboard.html", {'status': status})

def save_session_name(request):
    try:
        if request.method == 'POST':
            name_field = request.POST['file_path']
            if Session.objects.filter(name=name_field).exists():
                return JsonResponse({"status": False})
            new_session = Session.objects.create(name=name_field)
            new_session.save()
            globalViews.session_ID = new_session
            globalViews.active_session = True
            globalViews.session_name = name_field
            # Send path to another function that retrieves and writes all data for each tag in a .csv
            return JsonResponse({"status": True})
    except Exception as e:
        print(e)
    return JsonResponse(data)

def update_session_time(request):
    if request.method == 'POST':
        time = request.POST['sessioncard']
        latest_time = TagLocation.objects.latest(tagID)
        return HttpResponse('')

def establish_connection(request):
    info = Connection.objects.get(connID=1)
    try:
        connect_to()
        info.connected = True
        info.save()
        print("MADE A CONNECTION SUCCESSFULLY")
        return JsonResponse({"status": True})
    except Exception as e:
        return JsonResponse({"status": False})
    return JsonResponse(data)

def teardown_connection(request):
    info = Connection.objects.get(connID=1)
    connect.tear_down()
    print("Decoupling")
    try:
        globalViews.active_session = False
        globalViews.session_name = None
        globalViews.session_ID = None

        globalViews.times_logged = 0
        info.connected = False
        info.save()
        return JsonResponse({"status": False})
    except Exception as e:
        return JsonResponse({"status": True})
    return JsonResponse(data)

def collect_tags(request):
    try:
        is_connected = Connection.objects.get(connID=1).connected
        zone_tags = find_zone(globalViews.received_stack)
        print("ZONE TAGS: ------>>>>> " + str(zone_tags))
        return JsonResponse({"status": is_connected, "tags": zone_tags, "logcount": globalViews.times_logged})
    except Exception as e:
        print(e)
    return JsonRespone(data)

def sent_data(arr):
    globalViews.received_stack = arr
    if globalViews.active_session:
        name = globalViews.session_name
        session = globalViews.session_ID
        for entry in arr:
            tag_ID = entry[0]
            if not Tag.objects.filter(tagID=tag_ID).exists():
                new_tag = Tag.objects.create(tagID=tag_ID, name="Tag#" + str(tag_ID))
                new_tag.save()
            location = TagLocation.objects.create(tagID=Tag.objects.get(tagID=tag_ID), sessionID=session, timestamp=entry[1], x_pos=entry[2], y_pos=entry[3], vx=entry[4], vy=entry[5])
            location.save()

def incremenet_log_count():
    globalViews.times_logged += 1

def floor_params(request):
    floor = Room.objects.get(roomID=1)
    zones = Zone.objects.filter(roomID=floor.roomID)
    return render(request, "floor_html/floor.html", {"floor": floor, "zones": zones})

def find_zone(live_tags):
    table_info = []

    floor = Room.objects.get(roomID=1)
    zones = Zone.objects.filter(roomID=floor.roomID)
    s = []
    for tag in live_tags:
        s = [tag[0], tag[1], "NaN"]
        tag_x = tag[2]
        tag_y = tag[3]
        for zone in zones:
            if tag_x > zone.x_start and tag_x < zone.x_end:
                if tag_y > zone.y_start and tag_y < zone.y_end:
                    s[2] = zone.name
        table_info.append(s)

    return table_info

def session(request):

    return render(request, "analysis_html/session.html" )
