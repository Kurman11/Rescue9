from django.shortcuts import render
from .models import Recipe, Comment, CommentImage
from .forms import RecipeForm, CommentForm, CommentImageForm
from accounts.models import User


# Create your views here.
def index(request):
    recipes = Recipe.object.all()
    context = {
        'recipes': recipes,
    }
    return render(request, 'recipes/recipes_index.html')


def create(request):
    if request.method == 'POST':
        Recipe_form = RecipeForm(data=request.POST, files=request.FILES)
        if Recipe_form.is_valid():
            recipe = Recipe_form.save(commit=False)
            return redirect('recipes:detail', recipe.pk)

    else:
        Recipe_form = RecipeForm()
    
    context = {
        'Recipe_form': Recipe_form,
    }
    return render(request, 'recipes/create.html', context)


def detail(request, recipe_pk: int):
    recipe = Recipe.objects.get(pk=recipe_pk)
    comments = recipe.comment_set.all()
    comment_form = CommentForm()
    comment_images = CommentImage.objects.filter(recipe = recipe)
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
            recipe = recipe_form.save(commit=False)
    else:
        recipe_form = RecipeForm(instance=recipe)

    context = {
        'recipe_form': recipe_form,
    }
    return render(request, 'recipes/update.html', context)


def recipe_like_users(request, recipe_pk):
    recipe = Recipe.objects.get(pk=recipe_pk)
    if recipe.like_users.filter(pk=request.user.pk).exist():
        recipe.like_users.remove(request.user)
    else:
        recipe.like_users.add(request.user)
    return redirect('recipes:detail')


def category(request, subject):
    subject = subject
    recipe = Recipe.objects.filter(category=subject)
    context = {
        'subject': subject,
        'recipes': recipes,
    }
    return render(request, 'recipes/category.html', context)


def comment_create(request, recipe_pk: int):
    recipe = Recipe.objects.get(pk=recipe_pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.recipe = recipe
        comment.recipe.user = request.user
        comment.save()
        return redirect('recipes:detail', recipe.pk)
    context = {
        'recipe': recipe,
        'comment_form': comment_form,
    }
    return render(request, 'recipes/detail.html', context)


def comment_update(request, recipe_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.user == comment.user:
        if request.method == 'POST':
            comment_form = CommentForm(request.POST, instance=comment)
            if comment_form.is_valid():
                comment_form.save()
                return redirect('recipes:detail', recipe_pk)
        else:
            comment_form = CommentForm(instance=comment)
        context = {
            'comment_form': comment_form,
            'comment': comment,
        }
        return render(request, 'recipes/detail.html', context)

def comment_delete(request, recipe_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.user == comment.user:
        comment.delete()

    return redirect('recipes:detail', recipe_pk)


def comment_like_users(request, recipe_pk, comment_pk):
    comment = comment.objects.get(pk=comment_pk)
    if request.user in comment.like_users.all():
        comment.like_users.remove(request.user)
    else:
        comment.like_users.add(request.user)
    return redirect('recipes:detail', recipe_pk)