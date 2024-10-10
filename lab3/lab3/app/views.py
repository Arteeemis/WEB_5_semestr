from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from app.serializers import WordCardsSerializer
from app.models import WordCards
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .minio import add_pic

class WordCardList(APIView):
    model_class = WordCards
    serializer_class = WordCardsSerializer

    # Возвращает список 
    def get(self, request, format=None):
        word_cards = self.model_class.objects.all()
        serializer = self.serializer_class(word_cards, many=True)
        return Response(serializer.data)

    # Добавляет новую 
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            word_card = serializer.save()
            pic = request.FILES.get('pic')
            pic_result = add_pic(word_card, pic)
            if 'error' in pic_result.data:    
                return pic_result
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WordCardDetail(APIView):
    model_class = WordCards
    serializer_class = WordCardsSerializer

    # Возвращает информацию об акции
    def get(self, request, pk, format=None):
        word_card = get_object_or_404(self.model_class, pk=pk)
        serializer = self.serializer_class(word_card)
        return Response(serializer.data)

    # Обновляет информацию об акции (для модератора)
    def put(self, request, pk, format=None):
        word_card = get_object_or_404(self.model_class, pk=pk)
        serializer = self.serializer_class(word_card, data=request.data, partial=True)
        if 'pic' in serializer.initial_data:
            pic_result = add_pic(word_card, serializer.initial_data['pic'])
            if 'error' in pic_result.data:
                return pic_result
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Удаляет информацию об акции
    def delete(self, request, pk, format=None):
        word_card = get_object_or_404(self.model_class, pk=pk)
        word_card.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Обновляет информацию об акции (для пользователя)    
@api_view(['Put'])
def put(self, request, pk, format=None):
    word_card = get_object_or_404(self.model_class, pk=pk)
    serializer = self.serializer_class(word_card, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
