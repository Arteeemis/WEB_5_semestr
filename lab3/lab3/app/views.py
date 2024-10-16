from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from app.serializers import WordCardsSerializer, WordListsSerializer, CardsListsSerializer, UserRegisterSerializer, ResolveWordList
from app.models import WordCards, WordLists, CardsLists, User
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .minio import add_pic, delete_pic
import datetime

SINGLE_USER = User(id=2, username='valeron', email='valeron@gmail.com', password='valeron_rox')
SINGLE_ADMIN = User(id=3, username='admin', email='admin@gmail.com', password='admin')

# Возвращает список карточек
@api_view(['GET'])
def get_word_cards(request, format=None):
    word_cards = WordCards.objects.all().order_by('word_level') # Используем модель WordCards
    word_list = get_object_or_404(WordLists, creator=SINGLE_USER.id, status='draft')
    cards = CardsLists.objects.filter(list=word_list).count()
    serializer = WordCardsSerializer(word_cards, many=True)
    data = {
        "word_list_id": word_list.id,
        "cards_in_list": cards,
        "cards": serializer.data
    }
    return Response(data)


# Возвращает информацию о карточке
@api_view(['GET'])
def get_word_card_info(request, pk, format=None):
  word_card = get_object_or_404(WordCards, pk=pk)
  serializer = WordCardsSerializer(word_card)
  return Response(serializer.data)


# Добавляет новую карточку
@api_view(['POST'])
def add_word_card(request, format=None):
  serializer = WordCardsSerializer(data=request.data)
  if serializer.is_valid():
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)
  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 


# Обновляет информацию о карточке  
@api_view(['PUT'])
def update_card_info(request, pk, format=None):
  word_card = get_object_or_404(WordCards, pk=pk)
  serializer = WordCardsSerializer(word_card, data=request.data, partial=True)
  if serializer.is_valid():
    serializer.save()
    return Response(serializer.data)
  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Удаляет карточку 
@api_view(['DELETE'])
def delete_card(request, pk, format=None):
  word_card = get_object_or_404(WordCards, pk=pk)
  delete_pic(word_card)
  word_card.delete()
  return Response(status=status.HTTP_204_NO_CONTENT)


# Добавляет картинку карточке
@api_view(['POST'])
def add_card_img(request, pk, format=None):
  word_card = get_object_or_404(WordCards, pk=pk)
  serializer = WordCardsSerializer(word_card)
  pic = request.FILES.get('pic')
  if pic:
    if word_card.word_image != 'null':
        delete_pic(word_card)
    pic_result = add_pic(serializer.instance, pic)
    if 'error' in pic_result.data:
        return pic_result
  return Response(status=status.HTTP_204_NO_CONTENT)


#добвить в список
@api_view(['POST'])
def add_to_list(request, pk):
    word_card = WordCards.objects.filter(id=pk).first()
    if word_card is None:
        return Response('No such card', status=status.HTTP_404_NOT_FOUND)
    req = WordLists.objects.filter(creator = SINGLE_USER.id, status='draft').first()
    if not(req):
      words_list = WordLists.objects.create(status="draft", creation_date=datetime.datetime.now().date())
      words_list.save()
      req = words_list
    word_list_id = req.id
    existing_cards_count = CardsLists.objects.filter(list=req).count()
    order = existing_cards_count + 1
    card_list = CardsLists.objects.filter(card=pk, list=word_list_id).first()
    if not card_list:
        list_card = CardsLists(card=word_card, list=req, lists_order=order)
        list_card.save()
    return Response('Succesfully added card to list')

#удалить из списка
@api_view(['DELETE'])
def delete_from_list(request, ck, lk):
    card_in_list = CardsLists.objects.filter(card=ck, list=lk).first()
    print(ck , lk)
    if card_in_list is None:
        return Response("Card not found", status=status.HTTP_404_NOT_FOUND)
    card_in_list.delete()
    # list_id = card_in_list.list
    # print(list_id)
    # card_id = card_in_list.card
    # word_list = WordLists.objects.filter(id=lk).first()
    # card = WordCards.objects.filter(id=ck).first()
    # word_list.save()
    return Response(status=status.HTTP_200_OK)

#изменить карточку в списке
@api_view(['PUT'])
def change_card_in_list(request, ck, lk):
    print(ck, lk)
    card_in_list = CardsLists.objects.filter(card=ck, list=lk).first()
    if card_in_list is None:
        return Response("Card not found", status=status.HTTP_404_NOT_FOUND)
    serializer = CardsListsSerializer(card_in_list, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response('Failed to change data', status=status.HTTP_400_BAD_REQUEST)


#Возращает информацию о заявке
@api_view(['GET'])
def get_word_list_info(request, pk, format=None):
    try:
        word_list = WordLists.objects.get(pk=pk)
    except WordLists.DoesNotExist:
        return Response({"error": "Список не найден"}, status=status.HTTP_404_NOT_FOUND)
    word_list_serializer = WordListsSerializer(word_list)
    cards_in_list = CardsLists.objects.filter(list=word_list).values_list('card', flat=True)
    word_cards = WordCards.objects.filter(pk__in=cards_in_list)
    word_cards_serializer = WordCardsSerializer(word_cards, many=True) # Сериализуем карточки
    cards_serializer = CardsListsSerializer(cards_in_list, many=True)
    data = {
        "word_list": word_list_serializer.data,
        "cards": word_cards_serializer.data # Теперь это карточки
    }
    return Response(data)


#редактирует заявку
@api_view(['PUT'])
def update_word_list(request, pk, format=None):
    try:
        word_list = WordLists.objects.get(pk=pk)
    except WordLists.DoesNotExist:
        return Response({"error": "Список не найден"}, status=status.HTTP_404_NOT_FOUND)
    serializer = WordListsSerializer(word_list, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#сформировать отправление
@api_view(['PUT'])
def form_list(request, pk):
  word_list = get_object_or_404(WordLists, pk=pk, status='draft')
  if word_list is None:
      return Response("No word_list ready for formation", status=status.HTTP_404_NOT_FOUND)

  time_to_learn = request.data.get('time_to_learn')
  if time_to_learn is None or time_to_learn == "":
      return Response("No time_to_learn written", status=status.HTTP_400_BAD_REQUEST)

  word_list.status = 'formed'
  word_list.submition_date = datetime.datetime.now().date()
  if time_to_learn == 'week':
    word_list.learn_until_date = (datetime.datetime.now() + datetime.timedelta(weeks=1)).date()
  elif time_to_learn == 'month':
      word_list.learn_until_date = (datetime.datetime.now() + datetime.timedelta(weeks=4)).date()
  else:
      return Response("Incorrect time_to_learn", status=status.HTTP_400_BAD_REQUEST)
  word_list.save()
  serializer = WordListsSerializer(word_list)
  return Response(serializer.data, status=status.HTTP_200_OK)


#завершить/отклонить модератором
@api_view(['PUT'])
def resolve_word_list(request, pk):
    word_list = WordLists.objects.filter(id=pk, status='formed').first()
    resolve_decision = request.data.get('resolve_status')
    if resolve_decision == 'complete':
       resolve_decision == 'completed'
    else:
       resolve_decision == 'cancelled'
    
    if word_list is None:
      return Response("No word list found", status=status.HTTP_404_NOT_FOUND)
    serializer = ResolveWordList(word_list,data=request.data,partial=True)
    if serializer.is_valid():
      serializer.save()
      word_list = WordLists.objects.get(id=pk)
      word_list.completion_date = datetime.datetime.now().date()
      word_list.moderator = SINGLE_ADMIN.id
      word_list.status = resolve_decision
      word_list.save()
      serializer = ResolveWordList(word_list)
      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response('Failed to resolve the list', status=status.HTTP_400_BAD_REQUEST)


#удалить заявку
@api_view(['DELETE'])
def delete_word_list(request, pk, format=None):
  try:
    word_list = WordLists.objects.get(pk=pk)
  except WordLists.DoesNotExist:
    return Response({"error": "Список не найден"}, status=status.HTTP_404_NOT_FOUND)
  word_list.status = "deleted"
  word_list.save()
  return Response(status=status.HTTP_204_NO_CONTENT)


#заявки
@api_view(['GET'])
def get_word_lists(request):
  # Получаем параметры из запроса
  status_filter = request.data.get('status')
  start_date_str = request.data.get('creation_date')
  end_date_str = request.data.get('completion_date')
  # Фильтруем по статусу (кроме "deleted" и "draft")
  word_lists = WordLists.objects.filter(status__in=['formed', 'completed', 'cancelled'])

  # Фильтруем по диапазону дат (если заданы)
  if start_date_str and end_date_str:
    try:
      start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
      end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
      word_lists = word_lists.filter(creation_date__range=[start_date, end_date])
    except ValueError:
      return Response({"error": "Неверный формат даты"}, status=status.HTTP_400_BAD_REQUEST)

  # Фильтруем по статусу (если задан)
  if status_filter:
    if status_filter != 'draft' and status_filter != 'deleted':
        word_lists = word_lists.filter(status=status_filter)

  serializer = WordListsSerializer(word_lists, many=True)
  return Response(serializer.data)



# Создание пользователя
@api_view(['POST'])
def register_user(request):
  serializer = UserRegisterSerializer(data=request.data)
  if serializer.is_valid():
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)
  return Response('Creation failed', status=status.HTTP_400_BAD_REQUEST)


#Вход
@api_view(['POST'])
def login_user(request):
    return Response('Login', status=status.HTTP_200_OK)



#деавторизация
@api_view(['POST'])
def logout_user(request):
    return Response('Logout', status=status.HTTP_200_OK)


#Обновление данных пользователя
@api_view(['PUT'])
def update_user(request, pk):
    user = User.objects.filter(id=pk).first()
    serializer = UserRegisterSerializer(user,data = request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response('Incorrect data', status=status.HTTP_400_BAD_REQUEST)
    