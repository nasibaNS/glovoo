from .models import *
from modeltranslation.translator import TranslationOptions,register

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('category_name',)


@register(Store)
class StoreTranslationOptions(TranslationOptions):
    fields = ('description', 'address')



@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('product_name', 'description')



@register(ProductCombo)
class ProductComboTranslationOptions(TranslationOptions):
    fields = ('combo_name', 'description')
