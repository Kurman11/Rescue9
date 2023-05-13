from django.shortcuts import render, redirect
from django.urls import reverse
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
    # comment_image_form = CommentImageForm(request.POST, request.FILES)
    reviews = recipe.review_set.all().order_by('-pk')

    session_key = 'recipe_{}_hits'.format(recipe_pk)
    if not request.session.get(session_key):
        recipe.hits += 1
        recipe.save()
        request.session[session_key] = True

    context = {
        'recipe': recipe,
        'reviews': reviews,
        'review_form': review_form,
        # 'comment_image_form': comment_image_form,
    }
    return render(request, 'recipes/detail.html', context)


def update(request, recipe_pk: int):
    recipe = Recipe.objects.get(pk=recipe_pk)
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


def delete(request, recipe_pk):
    recipe = Recipe.objects.get(pk=recipe_pk)
    if request.user == recipe.user:
        recipe.delete()
    return redirect('recipes:index')


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


def review_create(request, recipe_pk: int):
    recipe = Recipe.objects.get(pk=recipe_pk)
    review_form = ReviewForm(request.POST)
    # comment_image_form = CommentImageForm(request.POST, request.FILES)
    if review_form.is_valid():
        review = review_form.save(commit=False)
        review.recipe = recipe
        review.user = request.user
        review.save()

        # commentimage = comment_image_form.save(commit=False)
        # commentimage.comment = comment
        # commentimage.save()
        return redirect(reverse('recipes:detail', kwargs={"recipe_pk": recipe_pk}) + '#review-start')
        
    context = {
        'recipe': recipe,
        'review_form': review_form,
        # 'comment_image_form': comment_image_form,
    }
    return render(request, 'recipes/detail.html', context)


def review_update(request, recipe_pk, review_pk):
    review = Review.objects.get(pk=review_pk)
    if request.user == review.user:
        if request.method == 'POST':
            review_form = ReviewForm(request.POST, instance=review)
            # review_image_form = CommentImageForm(request.POST, request.FILES, instance=comment.commentimage_set.first())
            if review_form.is_valid():
                review_form.save()
                # comment_image_form.save()
                return redirect('recipes:detail', recipe_pk)
        else:
            review_form = ReviewForm(instance=review)
            # comment_image_form = CommentImageForm(instance=comment.commentimage_set.first())
        context = {
            'review_form': review_form,
            # 'comment_image_form': comment_image_form,
            'review': review,
        }
        return render(request, 'recipes/detail.html', context)


def review_delete(request, recipe_pk, review_pk):
    review = Review.objects.get(pk=review_pk)
    # comment_images = comment.commentimage_set.all()
    if request.user == review.user:
        # for comment_image in comment_images:
        #     comment_image.delete()
        review.delete()
    return redirect('recipes:detail', recipe_pk)


def review_like(request, recipe_pk, review_pk):
    review = Review.objects.get(pk=review_pk)
    if request.user in review.like_user.all():
        review.like_user.remove(request.user)
    else:
        review.like_user.add(request.user)
    return redirect('recipes:detail', recipe_pk)