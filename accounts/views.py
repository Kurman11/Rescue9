from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from .forms import CustomAuthenticationForm, CustomUserCreationForm, CustomUserChangeForm, CustomPasswordChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth import update_session_auth_hash
from django.core.paginator import Paginator
from recipes.models import Recipe, Review
from django.http import JsonResponse
from django.urls import reverse

# Create your views here.


def login(request):
    if request.user.is_authenticated:
        return redirect('products:index')

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            prev_url = request.session.get('prev_url')
            # 이전 페이지의 URL 정보가 있으면 해당 URL로 리다이렉트합니다.
            if prev_url:
                # 이전 페이지의 URL 정보를 삭제합니다.
                del request.session['prev_url']
                return redirect(prev_url)
            return redirect('products:index')
    else:
        form = CustomAuthenticationForm()
    request.session['prev_url'] = request.META.get('HTTP_REFERER')
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)


@login_required
def logout(request):
    auth_logout(request)
    request.session['prev_url'] = request.META.get('HTTP_REFERER')

    # 로그아웃 후 이전 페이지의 URL 정보가 있으면 해당 페이지로 리다이렉트합니다.
    prev_url = request.session.get('prev_url')
    if prev_url:
        # 이전 페이지의 URL 정보를 삭제합니다.
        del request.session['prev_url']
        return redirect(prev_url)
        
    return redirect('products:index')


def signup(request):
    if request.user.is_authenticated:
        return redirect('products:index')

    next_page = request.GET.get('next')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            auth_login(request, user)
            prev_url = request.session.get('prev_url')
            if prev_url:
                del request.session['prev_url']
                return redirect(prev_url)
            return redirect('products:index')
    else:
        form = CustomUserCreationForm()
    request.session['prev_url'] = request.META.get('HTTP_REFERER')
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)


@login_required
def delete(request):
    request.user.delete()
    auth_logout(request)
    return redirect('products:index')


@login_required
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile', request.user)
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/update.html', context)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('products:index')
    else:
        form = CustomPasswordChangeForm(request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/change_password.html', context)


def profile(request, username):
    User = get_user_model()
    person = User.objects.get(username=username)
    recipes = Recipe.objects.filter(user=person).order_by('-pk')
    review = Review.objects.filter(user=person).order_by('-pk')
    page= request.GET.get('page', '1')
    per_page = 5

    paginator = Paginator(recipes, per_page)
    paginator2 = Paginator(review, per_page)

    page_obj = paginator.get_page(page)
    page_obj2 = paginator2.get_page(page)
    context = {
        'person': person,
        'recipes' : page_obj,
        'reviews' : page_obj2,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def follow(request, user_pk):
    User = get_user_model()
    you = User.objects.get(pk=user_pk)
    me = request.user

    if you != me:
        if me in you.followers.all():
            you.followers.remove(me)
            is_followed = False
        else:
            you.followers.add(me)
            is_followed = True
        context = {
            'is_followed': is_followed,
            'followings_count': you.followings.count(),
            'followers_count': you.followers.count(),
        }
        return JsonResponse(context)
    return redirect('accounts:profile', you.username)

