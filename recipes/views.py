from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Recipe, Review
from .forms import RecipeForm, ReviewForm
from accounts.models import User
from django.conf import settings
from django.http import JsonResponse
from PIL import Image
import os
from django.core.files import File
from io import BytesIO
from products.models import Product
from django.core.paginator import Paginator
from django.db.models import Count, Avg, Sum

# Create your views here.
def index(request):
    recipes = Recipe.objects.all()
    recipes_like = Recipe.objects.annotate(num_likes=Count('like_users')).order_by('-num_likes')[:20]
    recipes_rating = Recipe.objects.annotate(avg_rating=Avg('review__rating')).order_by('-avg_rating')[:20]
    recipes_newproduct = Recipe.objects.filter(used_products__is_new=True).distinct()[:20]
    recipes_pricehigh = Recipe.objects.annotate(total_price=Sum('used_products__price')).order_by('-total_price')[:20]
    recipes_pricelow = Recipe.objects.annotate(total_price=Sum('used_products__price')).order_by('total_price')[:20]

    # 페이지 네이터 관련 항목
    page= request.GET.get('page', '1')
    per_page = 12
    paginator = Paginator(recipes, per_page)
    page_obj = paginator.get_page(page)

    context = {
        'recipes': recipes,
        'recipes_like': recipes_like,
        'recipes_rating': recipes_rating,
        'recipes_newproduct': recipes_newproduct,
        'recipes_pricehigh': recipes_pricehigh,
        'recipes_pricelow': recipes_pricelow,
        'recipes_page': page_obj,
    }
    return render(request, 'recipes/index.html', context)


@login_required
def create(request):
    products = Product.objects.all()
    if request.method == 'POST':
        recipe_form = RecipeForm(data=request.POST, files=request.FILES)
        if recipe_form.is_valid():
            recipe = recipe_form.save(commit=False)
            recipe.user = request.user
            
             # 이미지 crop 처리
            image_file = request.FILES.get('thumbnail_upload')
            crop_y = int(request.POST.get('crop_y'))
            container_height = int(request.POST.get('container_height'))
            print(crop_y)
            # 이미지 업로드 및 crop
            img = Image.open(image_file)
            real_y = (crop_y * img.height) / container_height
            real_crop_height = (img.height * 400) / container_height
            thumbnail_crop = img.crop((0, real_y, img.width, real_y + real_crop_height))
            file_extension = os.path.splitext(image_file.name)[1]
            save_path = f'thumbnail_crop/{os.path.basename(image_file.name)}{file_extension}'
            temp_file = BytesIO()
            thumbnail_crop.save(temp_file, format='JPEG')
            temp_file.seek(0)
            recipe.thumbnail_crop.save(save_path, File(temp_file))

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
        'products': products,
    }
    return render(request, 'recipes/create.html', context)


def detail(request, recipe_pk: int):
    recipe = Recipe.objects.get(pk=recipe_pk)
    review_form = ReviewForm()
    reviews = recipe.review_set.all().order_by('-pk')
    # 사진 있는 리뷰 - ProcessedImageField를 쓸 경우 사진이 없을 경우 none이 아니라 ''이다
    reviews_with_image = reviews.exclude(image='')
    # 평균 별점 구하기
    if reviews:
        average_rate = sum(review.rating for review in reviews) / len(reviews)
    else:
        average_rate = 0
    # recipe에 사용된 가격 총액 구하기
    total_price = sum(product.price for product in recipe.used_products.all())
    session_key = 'recipe_{}_hits'.format(recipe_pk)
    if not request.session.get(session_key):
        recipe.hits += 1
        recipe.save()
        request.session[session_key] = True

    context = {
        'recipe': recipe,
        'reviews': reviews,
        'review_form': review_form,
        'reviews_with_image': reviews_with_image,
        'average_rate': average_rate,
        'total_price': total_price,
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
                return redirect('recipes:detail', recipe_pk)
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
    if request.user != review.user:
        if request.user in review.like_user.all():
            review.like_user.remove(request.user)
            is_liked = False
        else:
            review.like_user.add(request.user)
            is_liked = True
        context = {
            'is_liked': is_liked,
            'likes_count': review.like_user.count(),
        }
        return JsonResponse(context)
    return redirect('recipes:detail', recipe_pk)