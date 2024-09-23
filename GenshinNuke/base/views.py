from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Character, Room, Weapon, Profile, get_video_id
from .forms import RoomForm, ProfileForm,CreateUserForm

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "The user does not exist.")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "The user or password is incorrect.")


    context = {'page':page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Error during register.")

    context = {'form': form}
    return render(request, 'base/login_register.html', context)

def home(request):
    character = request.GET.get('character') if request.GET.get('character') != None else ''
    weapon = request.GET.get('weapon') if request.GET.get('weapon') != None else ''
    damage = request.GET.get('damage') if request.GET.get('damage') != None else ''

    rooms = Room.objects.filter(Q(damage__icontains=damage) & Q(character__name__icontains=character) )
    print(character,weapon,damage)

    context = {'rooms':rooms, 'weapons':Weapon.objects.all(), 'room_count':rooms.count(), 'characters':Character.objects.all()}
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    if request.user.is_authenticated:
        room.view.add(request.user)

    context = {'room':room}
    return render(request, 'base/room.html', context)

def userProfile(request, pk):
    user = User.objects.get(username=pk)
    rooms = user.room_set.all()
    context = {'user':user, 'rooms':rooms}
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def updateProfile(request, pk):
    profile_id = User.objects.get(username=pk).id
    profile = Profile.objects.get(user_id=profile_id)
    form = ProfileForm(instance=profile)


    if request.user.id != profile_id:
        return HttpResponse("You do not have permission to perform this action.")

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/profile_form.html',context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()

    if request.method == 'POST':
        form = RoomForm(request.POST)

        if form.is_valid():
            #roomform
            room = form.save(commit=False)
            room.host = request.user
            room.proofURL = get_video_id(request.POST.get('proofURL'))
            room.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    room.proofURL = 'https://www.youtube.com/watch?v='+room.proofURL
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse("You do not have permission to perform this action.")
    
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            #roomform
            room = form.save(commit=False)
            room.proofURL = get_video_id(request.POST.get('proofURL'))

            room.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/room_form.html',context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse("You do not have permission to perform this action.")

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})

