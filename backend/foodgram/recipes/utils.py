from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from rest_framework.views import exception_handler

from .models import IngredientContent, ShoppingCart


def get_shopping_cart(request):
    """
    Create a string with sum for necessary ingredients
    for cooking recipes in shopping_cart.
    """
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
    sending_data = []
    for name, amount in summary.items():
        sending_data.append(f'{name}: {amount[0]} {amount[1]}')
    return sending_data


def create_pdf(canvas, data):
    pdfmetrics.registerFont(TTFont(
            'DejaVuSansCondensed',
            'recipes/DejaVuSansCondensed.ttf'
        )
        )
    canvas.setFont("DejaVuSansCondensed", 12)
    canvas.drawString(60, 750, 'Список покупок:')
    x, y = 40, 725
    for line in data:
        canvas.drawString(x, y, line)
        y -= 25
    canvas.showPage()
    canvas.save()


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if (
        context['request'].path == '/api/recipes/' and
        context['request'].method == 'POST' and
        response is not None
    ):
        fields_add = []
        fields_del = []
        for field in response.data:
            if isinstance(response.data[field][0], dict):
                fields_del.append(field)
                for subfield in response.data[field]:
                    if len(subfield) > 0:
                        for name, error in subfield.items():
                            fields_add.append((name, error))
        for field in fields_del:
            del response.data[field]
        for name, error in fields_add:
            response.data[name] = error
    return response
