from django.shortcuts import render,redirect
from products.models import Product
from recipes.models import Recipe
from django.db.models import Q
from products.forms import ProductForm

# Create your views here.


# def search(request):
#     query = request.GET.get('q', '')
#     # products = Product.objects.all()
#     # recipes = Recipe.objects.all()
#     if query:
#         search_recipe = Recipe.objects.filter(
#             Q(title__icontains=query) |
#             Q(user__username__icontains=query)
#         )
#         search_product = Product.objects.filter(
#             Q(product_name__icontains=query) |
#             Q(content__icontains=query)
#         )
#         # Article과 Product 검색 결과를 병합하여 리스트로 만듭니다.
#         # search_result = list(search_recipe) + list(search_product)
#         # 검색된 결과를 생성 시간을 기준으로 내림차순으로 정렬합니다.
#         # search_result.sort(key=lambda x: x.created_at, reverse=True)
#     # else:
#         # 검색어가 없을 경우에는 Article과 Product 전체를 생성 시간을 기준으로 내림차순으로 정렬합니다.
#         # search_result = list(Recipe.objects.all()) + list(Product.objects.all())
#         # search_result.sort(key=lambda x: x.created_at, reverse=True)
#     context = {
#         # 'search_result': search_result,
#         # 'products':products,
#         # 'recipes' : recipes,
#         'search_recipe': search_recipe,
#         'search_product' : search_product,
#     }
#     return render(request, 'searchs/search.html', context)

def search(request):
    query = request.GET.get('q', '')
    if query:
        search_recipe = Recipe.objects.filter(
            Q(title__icontains=query) |
            Q(user__username__icontains=query)
        )
        search_recipe2 = search_recipe.filter(
            Q(convenience_stores__name__icontains=query)
        )
        search_recipe3 = search_recipe.union(search_recipe2)
        
        search_product = Product.objects.filter(
            Q(name__icontains=query) |
            Q(category__icontains=query) | 
            Q(user__username__icontains=query)
        )
        search_product2 = Product.objects.filter(
            Q(convenience_stores__name__icontains=query)
        )
        search_product3 = search_product.union(search_product2)
        # search_convenience_stores = Product.objects.filter(
        #     Q(convenience_stores__name__icontains=query)
        # )
        # Article과 Product 검색 결과를 병합하여 리스트로 만듭니다.
        search_result_recipe = list(search_recipe3)
        search_result_product = list(search_product3)
        # search_result_convenience_stores = list(search_convenience_stores)
        # 검색된 결과를 생성 시간을 기준으로 내림차순으로 정렬합니다.
        # search_result.sort(key=lambda x: x.created_at, reverse=True)
    else:
    # 검색어가 없을 경우에는 Article과 Product 전체를 생성 시간을 기준으로 내림차순으로 정렬합니다.
        search_result_recipe = list(Recipe.objects.all())
        search_result_product = list(Product.objects.all())
        # search_result.sort(key=lambda x: x.created_at, reverse=True)
    context = {
        'search_result_recipe': search_result_recipe,
        'search_result_product': search_result_product,
        # 'search_result_convenience_stores' : search_result_convenience_stores,
    }
    return render(request, 'searchs/search.html', context)