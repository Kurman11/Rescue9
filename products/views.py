from django.shortcuts import render, redirect
from .models import Product, Review, Review_image
from .forms import ProductForm, ReviewForm, Review_imageForm
# Create your views here.

def index(request):
    products = Product.objects.all()[::-1]
    new_products = Product.objects.filter(is_new=True)[::-1]
    like_products = Product.objects.order_by('-like_users')
    hits_products = Product.objects.order_by('-hits')[:5]
    content = {
        'products':products,
        'new_products': new_products,
        'like_products':like_products,
        'hits_products' : hits_products,
    }
    return render(request, 'products/index.html', content)


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
    review_img = Review_imageForm(request.POST, request.FILES)
    reviews = product.review_set.all()

    session_key = 'product_{}_hits'.format(product_pk)
    if not request.session.get(session_key):
        product.hits += 1
        product.save()
        request.session[session_key] = True

    context ={
        'product' : product,
        'review_form' : review_form,
        'reviews' : reviews,
        'review_img' : review_img,
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
        review.product = product
        review.user = request.user
        review.save()

        # Review_image 모델 저장
        review_image = review_img.save(commit=False)
        review_image.review = review
        review_image.save()
        return redirect('products:detail', product.pk)
    context = {
        'product':product,
        'review_form': review_form,
        'review_img':review_img,
    }
    return render(request,'products/detail.html', context)

def review_update(request, product_pk, review_pk):
    review = Review.objects.get(pk=review_pk)
    if request.user == review.user:
        if request.method == 'POST':
            review_form = ReviewForm(request.POST, instance=review)
            review_img = Review_imageForm(request.POST, request.FILES, instance=review.review_image_set.first())
            if review_form.is_valid() and review_img.is_valid():
                review_img.save()
                review_form.save()
                return redirect('products:detail', product_pk)
        else:
            review_form = ReviewForm(instance=review)
            review_img = Review_imageForm(instance=review.review_image_set.first())
        context = {
            'review_img' : review_img,
            'review_form': review_form,
            'review': review,
        }
        return render(request, 'products/detail.html', context)


# def review_update(request, product_pk, review_pk):
#     review = Review.objects.get(pk=review_pk)
#     if request.user == review.user:
#         review_form = ReviewForm(request.POST, request.FILES, instance=review)
#         if review_form.is_valid():
#             review_form.save()
#             return redirect('products:detail', product_pk)
#         else:
#             review_form = ReviewForm(instance=review)
#         context = {
#             'review_form': review_form,
#             'review': review,
#         }
#         return render(request, 'products/detail.html', context)
    #     else:
    #         review_form = ReviewForm(instance=review)
    #     context = {
    #         'review' : review,
    #         'review_form' : review_form,
    #     }
    #     return render(request,'products/')

    # return redirect('products/detail.html', product_pk)

def review_delete(request,product_pk,review_pk):
    review = Review.objects.get(pk=review_pk)
    if request.user == review.user:
        review.delete()
        return redirect('products:detail', product_pk)
        

def review_likes(request,product_pk, review_pk):
    review = Review.objects.get(pk=review_pk)
    if review.like_users.filter(pk=request.user.pk).exists():
        review.like_users.remove(request.user)
    else:
        review.like_users.add(request.user)
    context={
        'review.like_users' : review.like_users,
    }
    return redirect('products:detail', product_pk)