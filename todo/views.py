from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .forms import TodoForm
from .models import Todo

# Create your views here.
def home(request):
    return render(request, "todo/home.html")

def signupuser(request):
    if request.method == "GET":
        return render(request, "todo/signupuser.html", {"form":UserCreationForm()})
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return(redirect("currenttodo"))
            except IntegrityError:
                return render(request, "todo/signupuser.html", {"form":UserCreationForm(), "error": "Username not available"}, )
        else:
            return render(request, "todo/signupuser.html", {"form":UserCreationForm(), "error": "Please choose matching passwords"}, )

def logoutuser(request):
    if request.method == "POST":
        logout(request)
        return(redirect("home"))
    
def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html', {'form':AuthenticationForm(), 'error':'Username and password did not match'})
        else:
            login(request, user)
            return redirect('currenttodo')


def createtodo(request):
    if request.method == "GET":
        return render(request, "todo/createtodo.html", {"form":TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return(redirect("currenttodo"))
        except ValueError:
            return render(request, "todo/createtodo.html", {"form":TodoForm(), "error": "Put in correct entries"})

def currenttodo(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, "todo/currenttodo.html", {"todos": todos})

def viewtodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk)
    return render(request, "todo/viewtodo.html", {"todo": todo})
