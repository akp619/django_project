from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required # "login_required" decorator is used to restrict pages which will be only accessible post login.
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .models import Room, Message, Topic
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_exempt       # """csrf_exempt""" is used to disable csrf protection for a specific view
from .forms import RoomForm, UserForm
from django.db.models import Q

# Create your views here
def home(request):

    # # if the user is already authenticated redirect the user to home page if they manually provide the path in th url
    # if request.user.is_authenticated:
    #     return redirect('home')
    req_param = request.GET.get('parameter')
    room_messages = Message.objects.all()
    rooms = {}
    if req_param == None or '':
        rooms = Room.objects.all()
        room_messages = Message.objects.all()
    else:
        # rooms = Room.objects.filter(topic__name=req_param)
        rooms = Room.objects.filter(
            Q(topic__name__icontains=req_param) |
            Q(name__icontains=req_param) |
            Q(description__icontains=req_param)
        )
        room_messages = Message.objects.filter(Q(room__topic__name__icontains=req_param))
    topics = Topic.objects.all()
    rooms_available_to_topics = {}
    for topic in topics:
        rooms_available_to_topics[topic.name] = len(Room.objects.filter(topic=topic))
    return render(request, "base_templates/home.html", {"rooms":rooms, "topics":rooms_available_to_topics, "room_messages":room_messages, "no_of_rooms": len(rooms), "rooms_available_to_topics":rooms_available_to_topics})

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = Room.objects.filter(host=pk) # get lists of dataset
    # filter(room__in = list(rooms.values_list('id', flat=True)))
    # filter > filter out the records
    # room__in > Message table with a column name "room" filter with list of ids match to "Message" table "room" column ex:- [1,2]
    room_messages = Message.objects.filter(room__in = list(rooms.values_list('id', flat=True)))
    topics = Topic.objects.all()
    context = {"user" : user, "rooms" : rooms, "room_messages":room_messages, "topics":topics}
    return render(request, "base_templates/user_profile.html", context)

def room(request, pk):
    if pk:
        # To get a single room object
        room = Room.objects.get(id=pk)

        participants = room.participants.all()
        if request.method == "POST":
            current_user = User.objects.get(username=request.user)
            if current_user.id not in list(participants.values_list('id', flat=True)):
                room.participants.add(current_user)
            message = Message.objects.create(user=request.user, room=room, body=request.POST.get('body'))
            return redirect("room", pk=room.id)
        if room:
            messages_data = Message.objects.filter(room=room.id).order_by('-created')
            return render(request, "base_templates/room.html", {"user": room.host,"room": room, "messages_data":messages_data, "participants":participants, "participants_count": len(participants)})
        return render(request, "base_templates/room.html", {"room": "Room Data not Found"})

# @csrf_exempt
# """@csrf_exempt""" decorator is used to disable csrf protection for a specific view
@login_required(login_url='userLogin') # page will be accessible once logged in
def createRoom(request):
    topics = Topic.objects.all()
    form = RoomForm()
    context = {"topics":topics, "form":form, "update": False}
    if request.method == "POST":
        topic_name = request.POST.get("topic")
        # method "get_or_create" will get the topic if existing or create a new topic instead
        topic, created = Topic.objects.get_or_create(name=topic_name)
        print(topic, created, "get_topic", "topic_created")
        new_room = Room.objects.create(
            host = request.user,
            name = request.POST.get("name"),
            description = request.POST.get("description"),
            topic = topic
        )
        print(new_room, "==new_room==")
        return redirect("home")

    """
        This below method is used to render a model with a default view with some default functionality
    """
    # form = RoomForm()
    # context = {"form":form}
    # if request.method == "POST":
    #     form = RoomForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    # room = form.save(commit=False)
    return render(request, "base_templates/room_form.html", context)

@login_required(login_url='userLogin') # page will be accessible once logged in
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'base_templates/room_form.html', context)

@login_required(login_url='userLogin') # page will be accessible once logged in
def delete(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse("You are not authorized to delete this room.")

    if request.method == "POST":
        room.delete()
        return redirect("home")
    return render(request, "base_templates/delete_room.html", {"room":room})

def userLogin(request):
    page = 'login'
    # if the user is already authenticated redirect the user to home page if they manually provide the path in th url
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST" and len(request.POST)>0:
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Username not found")

        user = authenticate(request, username=username, password=password)   # authenticating the user

        if user:
            login(request, user) # getting logged in to the system and a session is created
            return redirect("home")
        else:
            messages.error(request, "Username or password doesn't exist.")
    return render(request, "base_templates/login.html", {"page":page})

def userLogout(request):
    logout(request)
    return redirect("home")

def userRegister(request):
    page = 'register'
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid(): # checks all the data provided is valid or not
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save(commit=True)
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "An error occured during registration.")
    return render(request, "base_templates/user_register.html", {"page":page, "form":form})

@login_required(login_url='userLogin')
def userProfileUpdate(request, pk):
    user = User.objects.get(id=pk)
    form = UserForm(instance=user)

    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("home")
    context = {"form": form}
    return render(request, "base_templates/update_user_profile.html", context)

@login_required(login_url='userLogin')
def deleteMessage(request, pk, room_pk):
    message = Message.objects.get(id=pk)
    message.delete()
    return redirect("room", room_pk)

