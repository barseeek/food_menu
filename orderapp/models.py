from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from dateutil.relativedelta import relativedelta


# Create your models here.


class Product(models.Model):
    title = models.CharField(
        verbose_name='Название',
        max_length=100
    )
    allergy = models.ForeignKey(
        'Allergy',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Категория (аллергия)',
        related_name='products'
    )

    def __str__(self):
        return self.title


class Menu(models.Model):
    title = models.CharField(
        verbose_name='Тип меню',
        max_length=100
    )

    def __str__(self):
        return self.title


class Meal(models.Model):
    title = models.CharField(
        verbose_name='Категория (Время дня)',
        max_length=100
    )

    def __str__(self):
        return self.title


class Allergy(models.Model):
    title = models.CharField(
        verbose_name='Аллерген',
        max_length=100
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
    meal = models.ForeignKey(
        Meal,
        verbose_name='Категория (Время дня)',
        related_name='recipies',
        on_delete=models.CASCADE,
        null=True
    )
    calories = models.PositiveIntegerField(
        verbose_name='Общая калорийность',
        blank=True,
        default=0
    )
    menu = models.ForeignKey(
        Menu,
        verbose_name='Типы меню',
        related_name='recipies',
        on_delete=models.CASCADE,
        null=True
    )
    image = models.ImageField(
        verbose_name='Картинка',
        null=True,
    )

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
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    unit = models.CharField(
        verbose_name='Единица измерения (Количество)',
        max_length=100,
    )
    calories = models.FloatField(
        verbose_name='калории',
        blank=True,
        null=True
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
        max_length=100,
        choices=[(str(i), str(i)) for i in [1, 3, 6, 12]],
        default='1'
    )
    end = models.DateField(
        verbose_name='Конец подписки',
        editable=False
    )
    persons = models.CharField(
        verbose_name='Количество персон',
        max_length=100,
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
    breakfast = models.BooleanField(
        verbose_name='Включены завтраки',
        default=False
    )
    lunch = models.BooleanField(
        verbose_name='Включены обеды',
        default=False
    )
    dinner = models.BooleanField(
        verbose_name='Включены ужины',
        default=False
    )
    dessert = models.BooleanField(
        verbose_name='Включены дессерты',
        default=False
    )
    user = models.ForeignKey('CustomUser', verbose_name='Пользователь', on_delete=models.CASCADE, related_name='subsciptions')
    allergies = models.ManyToManyField(Allergy, verbose_name='Аллергии', related_name='allergies')

    def save(self, *args, **kwargs):
        self.end = self.start + relativedelta(months=int(self.months))
        super(Subscription, self).save(*args, **kwargs)

    def __str__(self):
        return f'Подписка {self.menu} для {self.user.username} {self.user.first_name} {self.user.last_name}'


class CustomUser(AbstractUser):
    pass
    # subscription = models.ForeignKey(
    #     Subscription,
    #     verbose_name='Подписка',
    #     related_name='users',
    #     on_delete=models.CASCADE,
    #     null=True,
    #     blank=True
    # )
