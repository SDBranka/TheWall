from django.shortcuts import render, redirect
from wall_app.models import User
from django.contrib import messages
import bcrypt

# Create your views here.

def index(request):
    return render(request, "index.html")

def register(request):
    if request.method == "POST": 
        errors = User.objects.register_validator(request.POST)
        if len(errors) > 0:
            for error in errors.values():
                messages.error(request, error)
            return redirect("/")
        else:
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()  # create the hash    
            user = User.objects.create(
                first_name = request.POST['first_name'],
                last_name = request.POST['last_name'],
                email = request.POST['email'],
                password=pw_hash
            ) 
            request.session['user_id'] = user.id
            return redirect("/wall")   
    else:
        return redirect("/")

def login(request):
    if request.method == "POST": 
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for error in errors.values():
                messages.error(request, error)
            return redirect("/")
        else:
            user = User.objects.get(email = request.POST['lemail'])
            if bcrypt.checkpw(request.POST['lpassword'].encode(), user.password.encode()):
                request.session['user_id'] = user.id
                return redirect("/wall")
            else:
                return redirect("/")
    else:
        return redirect("/")

# def success(request):
#     if not 'user_id' in request.session:
#         return redirect("/")

#     context = {
#         "logged_user": User.objects.get(id = request.session['user_id'])
#     }
#     return render(request, "success.html", context)

def logout(request):
    request.session.flush()
    return redirect("/")






