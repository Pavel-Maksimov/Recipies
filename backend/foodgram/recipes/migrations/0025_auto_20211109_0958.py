# Generated by Django 3.2.8 on 2021-11-09 09:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0024_alter_recipe_cooking_time'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='using_ingredients',
            new_name='ingredients',
        ),
        migrations.AlterField(
            model_name='ingredientcontent',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='using_ingredients', to='recipes.recipe'),
        ),
    ]
