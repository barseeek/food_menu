# Generated by Django 5.0.4 on 2024-05-14 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orderapp', '0009_alter_ingredient_unit_alter_meal_title_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='end',
            field=models.DateField(verbose_name='Конец подписки'),
        ),
    ]
