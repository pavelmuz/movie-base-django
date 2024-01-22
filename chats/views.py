from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from users.models import Profile
from .models import Message


@login_required(login_url='login')
def chats(request):
    profile = request.user.profile
    active_chats = Profile.objects.filter(
        Q(sent_messages__recipient=profile) |
        Q(recieved_messages__sender=profile)
    ).distinct()
    context = {
        'active_chats': active_chats
    }
    return render(request, 'chats/chats.html', context)


@login_required(login_url='url')
def chat(request, pk):
    current_user = request.user.profile
    recipient = Profile.objects.get(id=pk)
    messages = Message.objects.filter(
        (Q(sender=current_user) & Q(recipient=recipient)) |
        (Q(sender=recipient) & Q(recipient=current_user))
    ).order_by('timestamp')

    if request.method == 'POST':
        body = request.POST['chat-message']
        Message.objects.create(
            sender=current_user,
            recipient=recipient,
            body=body
        )
        return redirect('chat-details', pk)

    context = {
        'feed': messages,
        'recipient': recipient
    }
    return render(request, 'chats/chat-detail.html', context)
