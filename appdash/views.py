from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages

def index(request):
    return render(request,'index.html')


def register(request):
    print("***** 1 ")
    error = User.objects.basic_validator(request.POST)
    if len(error) > 0:
        print("***** 2 ")
        for key, value in error.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/')
    else:
        if request.method == "POST":
            print("***** 3 ")
            Register(request)
            print("***** 4 ")
        return redirect('/')

def login(request):
    error = User.objects.sigin_validator(request.POST)
    if len(error) > 0:
        print("***** 2 ")
        for key, value in error.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/')
    else:
        userId =  Login(request)
        print(userId)
        if userId!=None:
            request.session['userid'] = userId
            print("login : ",request.session['userid'])
            return redirect('/user_page')
        else:
            print('not Logged In')
            return redirect('/')

def user_page(request):
    if 'userid' in request.session :
        id = request.session['userid']
        user = User.objects.get(id = id)
        pypies = get_pypie(user)
        context = {
            "user" : user ,
            "pypies" : pypies,
        }
        return render(request,'user_page.html' , context)
    else:
        return redirect('/')

# user pypie page
def add_pypiy_by_user(request):
    error = User.objects.pypie_validator(request.POST)
    if len(error) > 0:
        print("***** 2 ")
        for key, value in error.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/user_page')
    else:
        if request.method == "POST":
            id = request.session['userid']
            user = User.objects.get(id = id)
            name = request.POST['name']
            filling = request.POST['filling']
            crust = request.POST['crust']
            print("1111")
            add_Pypie(name,filling,crust,user)
            print("2222")
            return redirect('/user_page')

# edit pypie page 
def edit_pypie_page(request,pypieId): 
    if 'userid' in request.session :
        pypie = get_one_pypie(pypieId)
        context = {
            "pypie" : pypie,
        }

        return render(request,'edit_pypie.html',context)
    else:
        return redirect('/')

# edit pypie data process
def edit_pypie_process(request,pypieId):
    pypie = Pypie.objects.get(id = pypieId)
    name = request.POST['name']
    filling = request.POST['filling']
    crust = request.POST['crust']
    edit_pypie(pypie,name,filling,crust)
    return redirect('/user_page')

# del pypie
def del_pypie_data(request,pypieId):
    del_pypie(pypieId)
    return redirect('/user_page')

# get all pypies
def pypies(request):
    if 'userid' in request.session :
        pypies = get_all_pypie(request)
        context = {
            "pypies" : pypies
        }
        return render(request,'pypies.html',context)
    else:
        return redirect('/')

# show pypie data
def show_pypie(request,pypieId):
    if 'userid' in request.session :
        pypie = get_one_pypie(pypieId)
        context = {
            "pypie" : pypie ,
        }
        return render(request,'show_pypie.html',context)
    else:
        return redirect('/')

# add vote
def vote(request,userId,pypieId):
    vote = 1
    vote_on(vote,userId,pypieId)
    return redirect('/pypies')

# del vote
def del_vote(request,userId,pypieId):
    vote = -1
    vote_on(vote,userId,pypieId)
    return redirect('/')


# logout
def log_out(request):
    request.session.flush()
    return redirect('/')
















