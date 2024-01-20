from django.shortcuts import render


def chats(request):
    context = {}
    return render(request, 'chats/chats.html', context)
