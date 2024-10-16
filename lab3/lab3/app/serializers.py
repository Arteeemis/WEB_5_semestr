from app.models import WordCards, WordLists, CardsLists, User
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
        

class WordListsSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = WordLists
        # Поля, которые мы сериализуем
        fields = [
                    'pk', 
                    'status' , 
                    'creation_date',
                    'submition_date', 
                    'completion_date',    
                    'creator',   
                    'moderator',  
                    'learn_until_date'  
                 ]
        

class CardsListsSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = CardsLists
        # Поля, которые мы сериализуем
        fields = [
                    'pk', 
                    'card',
                    'list',
                    'lists_order' 
                 ]
        

class UserRegisterSerializer(serializers.ModelSerializer):
  password = serializers.CharField(write_only=True)

  class Meta:
    model = User
    fields = ['username', 'email', 'password']

  def create(self, validated_data):
    user = User(**validated_data) # Сохраняем пароль без хеширования
    user.save()
    return user


class ResolveWordList(serializers.ModelSerializer):
    class Meta:
        model = WordLists
        fields = ['status']

