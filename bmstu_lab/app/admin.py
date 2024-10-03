from django.contrib import admin
from .models import WordLists, WordCards, CardsLists
# Register your models here.

admin.site.register(WordCards)
admin.site.register(WordLists)
admin.site.register(CardsLists)