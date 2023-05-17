from django.shortcuts import render, redirect
from .models import Product, Comment
from .forms import ProductForm, CommentForm
from django.http import JsonResponse
from taggit.models import Tag
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


# Create your views here.

def index(request):
    products = Product.objects.all()[::-1]
    new_products = Product.objects.filter(is_new=True)[::-1]
    like_products = Product.objects.order_by('-like_users')
    hits_products = Product.objects.order_by('-price')[:5]

    # 페이지 네이터 관련 항목
    page= request.GET.get('page', '1')
    per_page = 12
    paginator = Paginator(products, per_page)
    page_obj = paginator.get_page(page)

    content = {
        'products':page_obj,
        'new_products': new_products,
        'like_products':like_products,
        'hits_products' : hits_products,
    }
    return render(request, 'products/index.html', content)

@login_required
def create(request):
    if request.method == 'POST':
        tags = request.POST.get('tags').split(',')
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            for convenience_store in form.cleaned_data['convenience_stores']:
                product.convenience_stores.add(convenience_store)
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
    comments = product.comment_set.all()
    tags = product.tags.all()
    recipes = product.used_recipes.all().order_by('-like_users')


    session_key = 'product_{}_hits'.format(product_pk)
    if not request.session.get(session_key):
        product.hits += 1
        product.save()
        request.session[session_key] = True

    context ={
        'product' : product,
        'comment_form' : comment_form,
        'comments' : comments,
        'tags': tags,
        'recipes': recipes
    }
    return render(request,'products/detail.html', context)

@login_required
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

@login_required
def delete(request,product_pk):
    product = Product.objects.get(pk=product_pk)
    if request.user == product.user:
        product.delete()
    return redirect('products:index')

@login_required
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


from django.http import JsonResponse
@login_required
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


@login_required
def comment_update(request, product_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.user == comment.user:
        if request.method == 'POST':
            comment_form = CommentForm(request.POST, instance=comment)
            if comment_form.is_valid():
                comment_form.save()
                return redirect('products:detail', product_pk)
                # return JsonResponse({'status': 'success'})
        else:
            comment_form = CommentForm(instance=comment)
        context = {
            'comment_form': comment_form,
            'comment': comment,
        }
        return render(request, 'products/detail.html', context)
    

@login_required
def comment_delete(request, product_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.user == comment.user:
        comment.delete()

        return JsonResponse({'status': 'ok'})
    else:
        return JsonResponse({'status': 'error', 'message': '권한이 없습니다.'})



@login_required
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
        'like_users_list' : like_users_list,
        'r_is_like' :  r_is_like,
        'r_like_count' : r_like_count,
    }

    return JsonResponse(context)
