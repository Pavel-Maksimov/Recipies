import json

from recipes.models import Ingredient


file = open('../../data/ingredients.json', 'r')
units = []
for line in file:
    data = json.loads(line)
for item in data:
    print(item)
    Ingredient.objects.create(
        name=item['name'],
        measurement_unit=item['measurement_unit']
    )
