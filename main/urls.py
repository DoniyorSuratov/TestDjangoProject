from django.urls import path

from .views import ProductView, CookRecipes, RecipeDetails, RecipeIDView

urlpatterns = [
    path('', ProductView.as_view(), name='home'),
    path('recipes', CookRecipes.as_view(), name='recipes'),
    path('recipes-show', RecipeDetails.as_view(), name='show_reciept'),
    path('recipes-show/<int:product_id>', RecipeDetails.as_view(), name='show_reciept'),
    path('recipes-id', RecipeIDView.as_view(), name='recipes_id')
]