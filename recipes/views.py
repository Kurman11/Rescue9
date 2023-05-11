from django.shortcuts import render, redirect
from .models import Recipe, Comment, CommentImage
from .forms import RecipeForm, CommentForm, CommentImageForm
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
    comment_form = CommentForm()
    comment_image_form = CommentImageForm(request.POST, request.FILES)
    comments = recipe.comment_set.all()

    session_key = 'recipe_{}_hits'.format(recipe_pk)
    if not request.session.get(session_key):
        recipe.hits += 1
        recipe.save()
        request.session[session_key] = True

    context = {
        'recipe': recipe,
        'comments': comments,
        'comment_form': comment_form,
        'comment_image_form': comment_image_form,
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
    return render(request, 'recipes/index.html', context)


def comment_create(request, recipe_pk: int):
    recipe = Recipe.objects.get(pk=recipe_pk)
    comment_form = CommentForm(request.POST)
    comment_image_form = CommentImageForm(request.POST, request.FILES)
    if comment_form.is_valid() and comment_image_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.recipe = recipe
        comment.user = request.user
        comment.save()

        commentimage = comment_image_form.save(commit=False)
        commentimage.comment = comment
        commentimage.save()
        return redirect('recipes:detail', recipe.pk)
    context = {
        'recipe': recipe,
        'comment_form': comment_form,
        'comment_image_form': comment_image_form,
    }
    return render(request, 'recipes/detail.html', context)


def comment_update(request, recipe_pk, comment_pk):
    recipe = Recipe.objects.get(pk=recipe_pk)
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


def comment_like(request, recipe_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.user in comment.like_users.all():
        comment.like_users.remove(request.user)
    else:
        comment.like_users.add(request.user)
    return redirect('recipes:detail', recipe_pk)




from django.http import Http404
from django.http import JsonResponse
from PIL import Image

from django_ckeditor_5.views import image_verify, NoImageException, handle_uploaded_file
from django_ckeditor_5.forms import UploadFileForm


def upload_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        try:
            image_verify(request.FILES["upload"])
        except NoImageException as ex:
            return JsonResponse({"error": {"message": f"{str(ex)}"}})
        if form.is_valid():
            url = handle_uploaded_file(request.FILES["upload"])
            return JsonResponse({"url": url})
    raise Http404(_("Page not found."))
