from django.shortcuts import render, redirect
from .forms import UserRegForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from tests.models import NameTest, CountAnswer, SetTests


def reg(request):
    if request.method == 'POST':
        form = UserRegForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Пользователь {username} был успешно создан!')
            return redirect('index')

    else:
        form = UserRegForm

    form = UserRegForm()
    return render(request, 'users/reg.html', {'title': 'Страница регистрации', 'form': form})


@login_required
def profile(request):
    settests = SetTests.objects.all()
    user_answers = CountAnswer.objects.filter(user=request.user)
    return render(request, 'users/profile.html', {'settests':settests, 'user_answers': user_answers})
