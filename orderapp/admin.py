from django.contrib import admin

from orderapp.models import CustomUser, Subscription, Ingredient, Recipe, Menu, \
    Product, Meal


class IngredientInline(admin.TabularInline):
    model = Ingredient


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    pass


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    pass


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    pass


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [IngredientInline]


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Meal)
class CategoryAdmin(admin.ModelAdmin):
    pass
