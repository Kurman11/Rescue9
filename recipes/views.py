from django.shortcuts import render

# Create your views here.
def index(request):
    recipes = Recipe.object.all()
    context = {
        'recipes': recipes,
    }
    return render(request, 'recipes/recipes_index.html')