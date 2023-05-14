from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Recipe, Review
from .forms import RecipeForm, ReviewForm
from accounts.models import User
from django.conf import settings

# Create your views here.
def index(request):
    recipes = Recipe.objects.all()
    subject = '전체'
    context = {
        'subject': subject,
        'recipes': recipes,
    }
    return render(request, 'recipes/index.html', context)


@login_required
def create(request):
    if request.method == 'POST':
        recipe_form = RecipeForm(data=request.POST, files=request.FILES)
        if recipe_form.is_valid():
            recipe = recipe_form.save(commit=False)
            recipe.user = request.user
            recipe.save()
            recipe_form.save_m2m()
            return redirect('recipes:index')
        else:
            print(recipe_form.errors)
    else:
        recipe_form = RecipeForm()
    context = {
        'recipe_form': recipe_form,
        'media_url': settings.MEDIA_URL,
    }
    return render(request, 'recipes/create.html', context)


def detail(request, recipe_pk: int):
    recipe = Recipe.objects.get(pk=recipe_pk)
    review_form = ReviewForm()
    reviews = recipe.review_set.all().order_by('-pk')
    image_reviews = recipe.review_set.filter()
    ratings = Review.objects.all()
    total_rating = 0
    cnt = 0
    average_rating = 0
    for i in ratings:
        total_rating += i.rating
        cnt += 1
        average_rating = round((total_rating/cnt),1)
    session_key = 'recipe_{}_hits'.format(recipe_pk)
    if not request.session.get(session_key):
        recipe.hits += 1
        recipe.save()
        request.session[session_key] = True

    context = {
        'recipe': recipe,
        'reviews': reviews,
        'review_form': review_form,
        'image_reviews': image_reviews,
        'average_rating' : average_rating,
    }
    return render(request, 'recipes/detail.html', context)


@login_required
def update(request, recipe_pk: int):
    recipe = Recipe.objects.get(pk=recipe_pk)
    if request.user == recipe.user:
        if request.method == 'POST':
            recipe_form = RecipeForm(data=request.POST, files=request.FILES, instance=recipe)
            if recipe_form.is_valid():
                recipe = recipe_form.save()
                return redirect('recipes:datail', recipe_pk)
        else:
            recipe_form = RecipeForm(instance=recipe)

        context = {
            'recipe': recipe,
            'recipe_form': recipe_form,
        }
        return render(request, 'recipes/update.html', context)
    return redirect('accounts:login')


@login_required
def delete(request, recipe_pk):
    recipe = Recipe.objects.get(pk=recipe_pk)
    if request.user == recipe.user:
        recipe.delete()
    return redirect('recipes:index')


@login_required
def recipe_like(request, recipe_pk):
    recipe = Recipe.objects.get(pk=recipe_pk)
    if recipe.like_users.filter(pk=request.user.pk).exists():
        recipe.like_users.remove(request.user)
    else:
        recipe.like_users.add(request.user)
    return redirect('recipes:detail', recipe_pk)


def category(request, subject):
    subject = subject
    recipes = Recipe.objects.filter(category=subject)
    context = {
        'subject': subject,
        'recipes': recipes,
    }
    return render(request, 'recipes/index.html', context)


@login_required
def review_create(request, recipe_pk: int):
    recipe = Recipe.objects.get(pk=recipe_pk)
    review_form = ReviewForm(request.POST, request.FILES)
    if review_form.is_valid():
        review = review_form.save(commit=False)
        review.recipe = recipe
        review.user = request.user
        review.save()
        return redirect(reverse('recipes:detail', kwargs={"recipe_pk": recipe_pk}) + '#review-start')
        
    context = {
        'recipe': recipe,
        'review_form': review_form,
    }
    return render(request, 'recipes/detail.html', context)


@login_required
def review_update(request, recipe_pk, review_pk):
    review = Review.objects.get(pk=review_pk)
    if request.user == review.user:
        if request.method == 'POST':
            review_form = ReviewForm(request.POST, request.FILES, instance=review)
            if review_form.is_valid():
                review_form.save()
                return redirect('recipes:detail', recipe_pk)
        else:
            review_form = ReviewForm(instance=review)
        context = {
            'review_form': review_form,
            'review': review,
        }
        return render(request, 'recipes/detail.html', context)


@login_required
def review_delete(request, recipe_pk, review_pk):
    review = Review.objects.get(pk=review_pk)
    if request.user == review.user:
        review.delete()
    return redirect('recipes:detail', recipe_pk)


@login_required
def review_like(request, recipe_pk, review_pk):
    review = Review.objects.get(pk=review_pk)
    if request.user in review.like_user.all():
        review.like_user.remove(request.user)
    else:
        review.like_user.add(request.user)
    return redirect('recipes:detail', recipe_pk)