# Generated by Django 3.2.8 on 2021-10-28 15:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0007_auto_20211028_1545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientcontent',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredient_content', to='recipes.recipe'),
        ),
    ]
