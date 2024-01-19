from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def notifications(request):
    context = {}
    return render(request, 'notifications/notifications.html', context)
