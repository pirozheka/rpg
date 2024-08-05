from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404, redirect
from .models import Advertisement, Response
from .forms import AdvertisementForm, ResponseForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User

#Главная
def index(request):
    advertisements_list = Advertisement.objects.all()
    paginator = Paginator(advertisements_list, 15)  # Пагинация - 15 объявлений

    page = request.GET.get('page')
    try:
        advertisements = paginator.page(page)
    except PageNotAnInteger:
        advertisements = paginator.page(1)
    except EmptyPage:
        advertisements = paginator.page(paginator.num_pages)

    response_forms = {ad.id: ResponseForm() for ad in advertisements}

    context = {
        'advertisements': advertisements,
        'response_forms': response_forms,
    }
    return render(request, 'board/index.html', context)

#Создать объявление
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

#Создание комментария
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
                'Новый ответ: RPG',
                f'Получен новый ответ на ваше объявление "{advertisement.title}".',
                settings.EMAIL_HOST_USER,
                [advertisement.user.email],
                fail_silently=False,
            )
            return redirect('advertisement_detail', pk=advertisement.pk)
    else:
        form = ResponseForm()
    return render(request, 'board/create_response.html', {'form': form, 'advertisement': advertisement})


@login_required
def delete_response(request, pk):
    response = get_object_or_404(Response, pk=pk)
    if response.advertisement.user == request.user:
        response.delete()
    return redirect('user_dashboard')

@login_required
def accept_response(request, pk):
    response = get_object_or_404(Response, pk=pk)
    if response.advertisement.user == request.user:
        response.accepted = True
        response.save()
        send_mail(
            'Ваш отклик принят',
            f'Ваш отклик на объявление "{response.advertisement.title}" был принят.',
            settings.EMAIL_HOST_USER,
            [response.user.email],
            fail_silently=False,
        )
    return redirect('user_dashboard')


#Пользовательская страница
def user_dashboard(request):
    # Получение данных
    user_advertisements = Advertisement.objects.filter(user=request.user).order_by('-created_at')
    advertisement_paginator = Paginator(user_advertisements, 5)  # 5 на страницу

    page = request.GET.get('page')
    try:
        advertisements = advertisement_paginator.page(page)
    except PageNotAnInteger:
        advertisements = advertisement_paginator.page(1)
    except EmptyPage:
        advertisements = advertisement_paginator.page(advertisement_paginator.num_pages)

    # Получение комментов
    user_responses = Response.objects.filter(user=request.user).order_by('-created_at')
    response_paginator = Paginator(user_responses, 5)

    response_page = request.GET.get('response_page')
    try:
        responses = response_paginator.page(response_page)
    except PageNotAnInteger:
        responses = response_paginator.page(1)
    except EmptyPage:
        responses = response_paginator.page(response_paginator.num_pages)

    context = {
        'advertisements': advertisements,
        'responses': responses,
    }

    return render(request, 'board/user_dashboard.html', context)
