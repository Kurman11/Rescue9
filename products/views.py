from django.shortcuts import render, redirect
from .models import Product, Comment
from .forms import ProductForm, CommentForm
from django.http import JsonResponse
from taggit.models import Tag

# Create your views here.

def index(request):
    products = Product.objects.all()[::-1]
    new_products = Product.objects.filter(is_new=True)[::-1]
    like_products = Product.objects.order_by('-like_users')
    hits_products = Product.objects.order_by('-price')[:5]

    content = {
        'products':products,
        'new_products': new_products,
        'like_products':like_products,
        'hits_products' : hits_products,
    }
    return render(request, 'products/index.html', content)


def create(request):
    if request.method == 'POST':
        tags = request.POST.get('tags').split(',')
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            for tag in tags:
                product.tags.add(tag.strip())
            return redirect('products:detail', product.pk)
    else:
        form = ProductForm()
    context = {
        'form' : form,
    }
    return render(request, 'products/create.html', context)


def detail(request, product_pk):
    product = Product.objects.get(pk=product_pk)
    comment_form = CommentForm()
    # review_img = Review_imageForm(request.POST, request.FILES)
    comments = product.comment_set.all()
    tags = product.tags.all()

    session_key = 'product_{}_hits'.format(product_pk)
    if not request.session.get(session_key):
        product.hits += 1
        product.save()
        request.session[session_key] = True

    context ={
        'product' : product,
        'comment_form' : comment_form,
        'comments' : comments,
        # 'review_img' : review_img,
        'tags': tags,
    }
    return render(request,'products/detail.html', context)


def update(request, product_pk):
    product = Product.objects.get(pk=product_pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            tags = request.POST.get('tags').split(',')
            for tag in tags:
                product.tags.add(tag.strip())
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
    if product.like_users.filter(pk=request.user.pk).exists():
        product.like_users.remove(request.user)
        is_liked = False
    else:
        product.like_users.add(request.user)
        is_liked = True
    context = {
        'is_liked': is_liked,
        'like_count': product.like_users.count(),
    }
    return JsonResponse(context)
    # return redirect('products:detail', product.pk)


from django.http import JsonResponse

def comment_create(request, product_pk):
    product = Product.objects.get(pk=product_pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.product = product
        comment.user = request.user
        comment.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'errors': comment_form.errors})

# def comment_create(request, product_pk):
#     product = Product.objects.get(pk=product_pk)
#     comment_form = CommentForm(request.POST)
#     # review_img = Review_imageForm(request.POST, request.FILES)
#     if comment_form.is_valid():
#         comment = comment_form.save(commit=False)
#         comment.product = product
#         comment.user = request.user
#         comment.save()

#         # Review_image 모델 저장
#         # review_image = review_img.save(commit=False)
#         # review_image.review = review
#         # review_image.save()
#         return redirect('products:detail', product.pk)
#     context = {
#         'product':product,
#         'comment_form': comment_form,
#         # 'review_img':review_img,
#     }
#     return render(request,'products/detail.html', context)

def comment_update(request, product_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.user == comment.user:
        if request.method == 'POST':
            comment_form = CommentForm(request.POST, instance=comment)
            # review_img = Review_imageForm(request.POST, request.FILES, instance=review.review_image_set.first())
            if comment_form.is_valid():
                # review_img.save()
                comment_form.save()
                return redirect('products:detail', product_pk)
        else:
            comment_form = CommentForm(instance=comment)
            # review_img = Review_imageForm(instance=review.review_image_set.first())
        context = {
            # 'review_img' : review_img,
            'comment_form': comment_form,
            'comment': comment,
        }
        return render(request, 'products/detail.html', context)

def comment_delete(request, product_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.user == comment.user:
        comment.delete()

        # AJAX 요청에 대한 응답으로 JSON 객체를 반환합니다.
        return JsonResponse({'status': 'ok'})
    else:
        # 권한이 없는 경우 에러를 반환합니다.
        return JsonResponse({'status': 'error', 'message': '권한이 없습니다.'})


# def comment_delete(request,product_pk,comment_pk):
#     comment = Comment.objects.get(pk=comment_pk)
#     if request.user == comment.user:
#         comment.delete()
#         return redirect('products:detail', product_pk)
        



def comment_likes(request,product_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if comment.like_users.filter(pk=request.user.pk).exists():
        comment.like_users.remove(request.user)
        r_is_like = False
    else:
        comment.like_users.add(request.user)
        r_is_like = True
    r_like_count = comment.like_users.count()
    like_users_list = list(comment.like_users.all().values())
    context={
        # 'review.like_users' : review.like_users,
        'like_users_list' : like_users_list,
        'r_is_like' :  r_is_like,
        'r_like_count' : r_like_count,
    }

    return JsonResponse(context)
    # return redirect('products:detail', product_pk)
