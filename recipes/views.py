from django.shortcuts import render, redirect
from .models import Recipe, Comment, CommentImage
from .forms import RecipeForm, CommentForm, CommentImageForm
from accounts.models import User


# Create your views here.
def index(request):
    recipes = Recipe.objects.all()
    context = {
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
            return redirect('recipes:detail', recipe.pk)
    else:
        recipe_form = RecipeForm()
    context = {
        'recipe_form': recipe_form,
    }
    return render(request, 'recipes/create.html', context)


def detail(request, recipe_pk: int):
    recipe = Recipe.objects.get(pk=recipe_pk)
    comments = recipe.comment_set.all()
    comment_form = CommentForm()
    comment_images = CommentImageForm(request.POST, request.FILES)
    context = {
        'recipe': recipe,
        'comments': comments,
        'comment_form': comment_form,
        'comment_images': comment_images,
    }
    return render(request, 'recipe/detail.html', context)


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
        'recipe_form': recipe_form,
    }
    return render(request, 'recipes/update.html', context)


def delete(request, recipe_pk):
    recipe = Recipe.objects.get(pk=recipe_pk)
    if request.user == recipe.user:
        recipe.delete()
    return redirect('recipes:index')


def recipe_like_users(request, recipe_pk):
    recipe = Recipe.objects.get(pk=recipe_pk)
    if recipe.like_users.filter(pk=request.user.pk).exist():
        recipe.like_users.remove(request.user)
    else:
        recipe.like_users.add(request.user)
    return redirect('recipes:detail')


def category(request, subject):
    subject = subject
    recipes = Recipe.objects.filter(category=subject)
    context = {
        'subject': subject,
        'recipes': recipes,
    }
    return render(request, 'recipes/category.html', context)


def comment_create(request, recipe_pk: int):
    recipe = Recipe.objects.get(pk=recipe_pk)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        comment_image_form = CommentImageForm(request.POST, request.FILES)
        files = request.FILES.getlist('image')
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.recipe = Recipe.objects.get(pk=recipe_pk)
            comment.recipe.user = request.user
            comment.save()

            for file in files:
                CommentImage.objects.create(comment=comment, image=file)

            return redirect('recipes:detail', recipe_pk)
    else:
        comment_form = CommentForm()
        comment_image_form = CommentImageForm()

    context = {
        'recipe': recipe,
        'comment_form': comment_form,
        'comment_image_form': comment_image_form,
    }
    return render(request, 'recipes/detail.html', context)


def comment_update(request, recipe_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.user == comment.user:
        if request.method == 'POST':
            comment_form = CommentForm(request.POST, instance=comment)
            files = request.FILES.getlist('image')
            if comment_form.is_valid():
                comment_form.save()
                comment_images = CommentImage.objects.filter(comment=comment)
                for comment_image in comment_images:
                    comment_image.delete()
                for file in files:
                    CommentImage.objects.create(recipe=recipe, image=file)
                return redirect('recipes:detail', comment.recipe.pk)
        else:
            comment_form = CommentForm(instance=comment)
            comment_image_form = CommentImageForm()
        context = {
            'comment_form': comment_form,
            'comment_image_form': comment_image_form,
            'comment': comment,
        }
        return render(request, 'recipes/detail.html', context)




def comment_delete(request, recipe_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    comment_images = comment.commentimage_ser.all()
    if request.user == comment.user:
        for comment_image in comment_images:
            comment_image.delete()
        comment.delete()
    return redirect('recipes:detail', recipe_pk)


def comment_like_users(request, recipe_pk, comment_pk):
    comment = comment.objects.get(pk=comment_pk)
    if request.user in comment.like_users.all():
        comment.like_users.remove(request.user)
    else:
        comment.like_users.add(request.user)
    return redirect('recipes:detail', recipe_pk)