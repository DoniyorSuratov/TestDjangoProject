from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404,redirect
from django.views import View

from django.http import JsonResponse
from main.models import Recipe, RecipeProduct, Product
from django.db.models import F


class ProductView(View):
    template_name = 'index.html'
    context = {}

    def get(self, request):

        return render(request, self.template_name, self.context)
    def post(self, request):
        recipe_id = request.POST.get('recipe_id')
        product_id = request.POST.get('product_id')
        weight = request.POST.get('weight')

        recipe = RecipeProduct.objects.filter(product_id=product_id, recipe_id=recipe_id).first()
        check_product = Product.objects.filter(id=product_id).first()
        check_recipe = Recipe.objects.filter(id=recipe_id).first()
        if check_product and check_recipe:
            if recipe:

                recipe.weight_in_grams = weight
                recipe.save()
            else:

                recipe = RecipeProduct.objects.create(
                    recipe_id=recipe_id,
                    product_id=product_id,
                    weight_in_grams=weight
                )
        else:
            return JsonResponse({"success": False, "message": "Product or recipe not found"})


        return render(request, self.template_name,  self.context)



class CookRecipes(View):
    template_name = 'cook_recipes.html'
    context = {}

    def get(self, request):

        return render(request, self.template_name, self.context)
    def post(self, request):
        recipe_id = request.POST.get('recipe_id')
        query = RecipeProduct.objects.filter(recipe_id=recipe_id).values_list('product_id', flat=True)
        Product.objects.filter(id__in=query).update(times_cooked=F('times_cooked') + 1)

        return render(request, self.template_name,  self.context)


class RecipeDetails(View):
    template_name = 'recipet_details.html'
    context={}
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)

        recipes = Recipe.objects.filter(recipeproduct__product_id=product_id, recipeproduct__weight_in_grams__lt=10).all()


        context = {'product': product, 'recipes': recipes}
        return render(request, self.template_name, context)

class RecipeIDView(View):
    template_name = 'recipe_id.html'
    context={}
    def get(self, request):

        return render(request, self.template_name, self.context)


    def post(self, request):
        product_id = request.POST.get('product_id')
        check_product = Product.objects.filter(id=product_id).first()
        if check_product:
            return redirect(f'recipes-show/{product_id}' )
        else:
            return render(request, self.template_name, self.context)
