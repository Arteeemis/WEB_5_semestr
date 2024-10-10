from app.models import WordCards
from rest_framework import serializers

class WordCardsSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = WordCards
        # Поля, которые мы сериализуем
        fields = [
                    'pk',
                    'status',
                    'word',
                    'word_level',
                    'word_language',
                    'word_class',
                    'word_description',
                    'word_translation',
                    'word_example',
                    'word_synonyms',
                    'word_image',
                 ]
