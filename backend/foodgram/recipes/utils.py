from .models import IngredientContent, ShoppingCart


def get_shopping_cart(request):
    summary = dict()
    shopping_cart = ShoppingCart.objects.filter(user=request.user)
    for wish in shopping_cart:
        recipe_content = IngredientContent.objects.filter(
            recipe=wish.recipe
        )
        for content in recipe_content:
            ingr = content.ingredient
            if ingr not in summary:
                summary[ingr.name] = [content.amount, ingr.measurement_unit]
            else:
                summary[ingr.ingredient.name][0] += content.amount
    sending_data = 'Список покупок:\n\n'
    for name, amount in summary.items():
        sending_data += f'{name}: {amount[0]} {amount[1]}\n'
    return sending_data
