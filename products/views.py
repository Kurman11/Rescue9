from django.shortcuts import render, redirect
from .models import Product, Review, Review_image
from .forms import ProductForm, ReviewForm, Review_imageForm
# Create your views here.

def index(request):
    return render(request, 'products/index.html')


def create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            return redirect('products:detail', product.pk)
    else:
        form = ProductForm()
    context = {
        'form' : form,
    }
    return render(request, 'products/create.html', context)


def detail(request, product_pk):
    product = Product.objects.get(pk=product_pk)
    review_form = ReviewForm()
    reviews = product.review_set.all()
    context ={
        'product' : product,
        'review_form' : review_form,
        'reviews' : reviews,
    }
    return render(request,'products/detail.html', context)

def update(request, product_pk):
    product = Product.objects.get(pk=product_pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products:detail', product.pk)
    else:
        form = ProductForm(instance=product)
    context = {
        'product':product,
        'form' : form
    }
    return render(request,'products/update.html',context)

def delete(request,product_pk):
    product = Product.objects.get(pk=product_pk)
    if request.user == product.user:
        product.delete()
    return redirect('products:index')


def likes(request, product_pk):
    product = Product.objects.get(pk=product_pk)
    if product.like_users.filter(request.user):
        product.like_users.remove(request.user)
    else:
        product.like_users.add(request.user)
    return redirect('products:detail')


def review_create(request, product_pk):
    product = Product.objects.get(pk=product_pk)
    review_form = ReviewForm(request.POST)
    review_img = Review_imageForm(request.POST, request.FILES)
    if review_form.is_valid() and review_img.is_valid():
        review = review_form.save(commit=False)
        review.product_id = product
        review.user = request.user

        # Review_image 모델 저장
        review_image = review_img.save(commit=False)
        review_image.review_id = review
        review_image.save()
        return redirect('products:detail', product.pk)
    context = {
        'product':product,
        'review_form': review_form,
        'review_img':review_img,
    }
    return render(request,'products/detail.html', context)

# def review_create(request, product_pk):
#     product = Product.objects.get(pk=product_pk)
#     review_form = ReviewForm(request.POST)
#     review_img = Review_imageForm(request.POST, request.FILES)
#     if review_form.is_valid() and review_img.is_valid():
#         review = review_form.save(commit=False)
#         review.product_id = product
#         review.user = request.user
#         review.save()

#         review_image = review_img.save(commit=False)
#         review_image.review_id = review
#         review_image.save()

#         return redirect('products:detail', product.pk)
#     context = {
#         'product': product,
#         'review_form': review_form,
#         'review_img': review_img,
#     }
#     return render(request, 'products/detail.html', context)

# def review_create(request, product_pk):
#     product = Product.objects.get(pk=product_pk)
#     if request.method == 'POST':
#         review_form = ReviewForm(request.POST)
#         review_img = Review_imageForm(request.POST, request.FILES)
#         if review_form.is_valid() and review_img.is_valid():
#             review = review_form.save(commit=False)
#             review.product_id = product
#             review.user = request.user
#             review.save()

#             review_image = review_img.save(commit=False)
#             review_image.review_id = review
#             review_image.save()

#             return redirect('products:detail', product.pk)
#     else:
#         review_form = ReviewForm()
#         review_img = Review_imageForm()

#     context = {
#         'product': product,
#         'review_form': review_form,
#         'review_img': review_img,
#     }
#     return render(request, 'products/detail.html', context)