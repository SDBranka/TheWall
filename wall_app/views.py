from django.shortcuts import render, redirect
from .models import User, Message, Comment
from django.contrib import messages

# Create your views here.

def index(request):
    if not 'user_id' in request.session:
        return redirect("/")
    else:
        context = {
            "logged_user": User.objects.get(id = request.session['user_id']),
            "all_msgs": Message.objects.all().order_by("-created_at")
        }
    return render(request, "wall_index.html", context)


def add_msg(request):
    if not 'user_id' in request.session:
            return redirect("/")
    else:
        if request.method == "POST":
            errors = Message.objects.msg_validator(request.POST)
            if len(errors) > 0:
                for error in errors.values():
                    messages.error(request, error)
                return redirect("/wall")
            user_posting = User.objects.get(id = request.session['user_id'])
            Message.objects.create(
                msg_poster = user_posting,
                msg_content = request.POST['msg_content']
            )
            return redirect("/wall")
        else:
            return redirect("/wall")


def add_comment(request):
    if not 'user_id' in request.session:
            return redirect("/")
    else:
        if request.method == "POST":
            user_posting_cmt = User.objects.get(id = request.session['user_id'])
            msg_receiving_cmt = Message.objects.get(id = request.POST['message_id'])
            Comment.objects.create(
                cmt_poster = user_posting_cmt,
                cmt_message = msg_receiving_cmt,
                cmt_content = request.POST['cmt_content']
            )
            return redirect("/wall")
        else:
            return redirect("/wall")


def delete_msg(request):
    if not 'user_id' in request.session:
            return redirect("/")
    else:
        if request.method == "POST":
            msg_to_delete = Message.objects.get(id = request.POST['message_to_delete_id'])
            msg_to_delete.delete()
            return redirect("/wall")
        else:
            return redirect("/wall")

