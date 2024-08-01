from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import Advertisement, Response
from .forms import AdvertisementForm, ResponseForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings


def index(request):
    return render(request, 'board/index.html')

@login_required
def create_advertisement(request):
    if request.method == 'POST':
        form = AdvertisementForm(request.POST)
        if form.is_valid():
            advertisement = form.save(commit=False)
            advertisement.user = request.user
            advertisement.save()
            return redirect('advertisement_detail', pk=advertisement.pk)
    else:
        form = AdvertisementForm()
    return render(request, 'board/create_advertisement.html', {'form': form})

def advertisement_detail(request, pk):
    advertisement = get_object_or_404(Advertisement, pk=pk)
    return render(request, 'board/advertisement_detail.html', {'advertisement': advertisement})

@login_required
def create_response(request, pk):
    advertisement = get_object_or_404(Advertisement, pk=pk)
    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.user = request.user
            response.advertisement = advertisement
            response.save()
            send_mail(
                'New Response Received',
                f'You have a new response to your advertisement "{advertisement.title}".',
                settings.EMAIL_HOST_USER,
                [advertisement.user.email],
                fail_silently=False,
            )
            return redirect('advertisement_detail', pk=advertisement.pk)
    else:
        form = ResponseForm()
    return render(request, 'board/create_response.html', {'form': form})
