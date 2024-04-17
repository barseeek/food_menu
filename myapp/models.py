from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from dateutil.relativedelta import relativedelta

# Create your models here.


class Product(models.Model):
    title = models.CharField(
        verbose_name='Название',
        max_length=25
    )
    calories = models.PositiveIntegerField(
        verbose_name='ккал/100г'
    )
    category = models.CharField(
        verbose_name='Категория (Аллергии)',
        max_length=25,
        choices=(
            ('Нет', 'Нет'),
            ('Рыба и морепродукты', 'Рыба и морепродукты'),
            ('Мясо', 'Мясо'),
            ('Зерновые', 'Зерновые'),
            ('Продукты пчеловодства', 'Продукты пчеловодства'),
            ('Орехи и бобовые', 'Орехи и бобовые'),
            ('Молочные продукты', 'Молочные продукты'),
        ),
        default='Нет'
    )

    def __str__(self):
        return self.title


class Menu(models.Model):
    title = models.CharField(
        verbose_name='Тип меню',
        max_length=25
    )

    def __str__(self):
        return self.title


class Recipe(models.Model):
    title = models.CharField(
        verbose_name='Название',
        max_length=100
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    category = models.CharField(
        verbose_name='Категория (Время дня)',
        max_length=25,
        choices=(
            ('Нет', 'Нет'),
            ('Завтрак', 'Завтрак'),
            ('Обед', 'Обед'),
            ('Ужин', 'Ужин'),
            ('Десерт', 'Десерт')
        ),
        default='Нет'
    )
    calories = models.PositiveIntegerField(
        verbose_name='Общая калорийность'
    )
    menus = models.ManyToManyField(
        Menu,
        verbose_name='Типы меню',
        related_name='recipies'
    )

    def save(self, *args, **kwargs):
        ingredients = self.ingredients.all()
        calories = [
            (
                ingredient.product.calories *
                ingredient.quantity *
                ingredient.grams /
                100
            ) for ingredient in ingredients
        ]
        self.calories = sum(calories)
        super(Subscription, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    product = models.ForeignKey(
        Product,
        verbose_name='Продукт',
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        related_name='ingredients',
        on_delete=models.CASCADE
    )
    unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=10,
    )
    quantity = models.PositiveIntegerField(
        verbose_name='Количество'
    )
    grams = models.PositiveIntegerField(
        verbose_name='Граммов в ед. измерения'
    )

    def __str__(self):
        return self.product.title


class Subscription(models.Model):
    start = models.DateField(
        verbose_name='Начало подписки',
        default=timezone.now
    )
    months = models.CharField(
        verbose_name='Количество месяцев',
        max_length=5,
        choices=[(str(i), str(i)) for i in [1, 3, 6, 12]],
        default='1'
    )
    end = models.DateField(
        verbose_name='Конец подписки',
        editable=False
    )
    persons = models.CharField(
        verbose_name='Количество персон',
        max_length=5,
        choices=[(str(i), str(i)) for i in range(1, 7)],
        default='1'
    )
    cost = models.PositiveIntegerField(
        verbose_name='Стоимость'
    )
    promocode = models.BooleanField(
        verbose_name='Промокод',
        default=False
    )
    menu = models.ForeignKey(
        Menu,
        verbose_name='Тип меню',
        on_delete=models.CASCADE,
        related_name='subscriptions'
    )

    def save(self, *args, **kwargs):
        self.end = self.start + relativedelta(months=int(self.months))
        super(Subscription, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.menu} - {self.pk}'


class CustomUser(AbstractUser):
    subscription = models.ForeignKey(
        Subscription,
        verbose_name='Подписка',
        related_name='users',
        on_delete=models.CASCADE,
        null=True
    )
