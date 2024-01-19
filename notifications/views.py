from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from users.models import Profile
from .models import Notification


@login_required(login_url='login')
def notifications(request):
    profile = Profile.objects.get(user=request.user)
    notifications_list = profile.notifications.all().order_by('-created')
    context = {
        'notifications': notifications_list
    }
    return render(request, 'notifications/notifications.html', context)


@login_required(login_url='login')
def delete_notification(request, pk):
    notification = Notification.objects.get(id=pk)
    notification.delete()
    return redirect('notifications')
