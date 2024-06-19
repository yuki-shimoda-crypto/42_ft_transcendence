from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls.exceptions import Http404

from .forms import ChatmessageCreateForm
from .models import ChatGroup


# Create your views here.
@login_required
def profile_view(request, username=None):
    if username:
        profile = get_object_or_404(get_user_model(), username=username)
        is_blocked = profile in request.user.block_users.all()
    else:
        try:
            profile = request.user.profile
            is_blocked = False
        except get_user_model().DoesNotExist:
            return redirect("account_login")
    return render(
        request, "chat/profile.html", {"profile": profile, "is_blocked": is_blocked}
    )


@login_required
def chat_view(request, chatroom_name=None):
    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
    chat_messages = chat_group.chat_messages.all()[:30]
    form = ChatmessageCreateForm()

    other_user = None
    if chat_group.is_private:
        if request.user not in chat_group.members.all():
            raise Http404()
        for member in chat_group.members.all():
            if member != request.user:
                other_user = member
                break

    is_blocked = other_user in request.user.block_users.all()

    if request.htmx:
        form = ChatmessageCreateForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.group = chat_group
            message.save()
            context = {
                "message": message,
                "user": request.user,
            }
            return render(request, "chat/partials/chat_message_p.html", context)

    context = {
        "chat_messages": chat_messages,
        "form": form,
        "other_user": other_user,
        "chatroom_name": chatroom_name,
        "is_blocked": is_blocked,
    }

    return render(request, "chat/chat.html", context)


@login_required
def get_or_create_chatroom(request, username):
    if request.user.username == username:
        return redirect("chat-home")

    User = get_user_model()
    other_user = User.objects.get(username=username)
    my_chatrooms = request.user.chat_groups.filter(is_private=True)

    if my_chatrooms.exists():
        for chatroom in my_chatrooms:
            if other_user in chatroom.members.all():
                chatroom = chatroom
                break
            chatroom = ChatGroup.objects.create(is_private=True)
            chatroom.members.add(other_user, request.user)

    else:
        chatroom = ChatGroup.objects.create(is_private=True)
        chatroom.members.add(other_user, request.user)

    return redirect("chatroom", chatroom.group_name)


def user_list(request):
    users = get_user_model().objects.exclude(id=request.user.id)
    return render(request, "chat/user_list.html", {"users": users})


def user_block_post(request, username):
    block_user = get_object_or_404(get_user_model(), username=username)
    is_blocked = block_user in request.user.block_users.all()

    if is_blocked:
        request.user.block_users.remove(block_user)
    else:
        request.user.block_users.add(block_user)
    request.user.save()
    return redirect("profile", username=username)