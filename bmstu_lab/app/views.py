from django.shortcuts import render, redirect
from django.http import HttpResponse
from app.models import WordLists, WordCards, CardsLists
from django.db.models import Q, F
from django.core.exceptions import BadRequest
from datetime import date, timedelta
from django.db import connection
import psycopg2
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse


# word_cards = [{
#           'id' : 1, 
#           'word': 'Persistent', 
#           'level' : 'C2',
#           'language' : 'Английский',
#           'word_class' : 'adjective/прилагательное', 
#           'description': 'A persistent person continues to do something although other people do not want them to.', 
#           'translation': 'настойчивый, упорный', 
#           'example' : "he was persistent and wouldn't leave me alone", 
#           'synonyms' : 'determined, perseverant', 
#           'image' : 'http://127.0.0.1:9000/lab1/persistent.png'},

#          {
#           'id': 2,
#           'word': 'Alegre',
#           'level': 'A1',
#           'language': 'Испанский', 
#           'word_class': 'adjetivo/прилагательное', 
#           'description': 'Una persona alegre se siente feliz y llena de energía.',
#           'translation': 'веселый, радостный',
#           'example': 'Ella siempre está alegre y sonriente.',
#           'synonyms': 'feliz, contento',
#           'image': 'http://127.0.0.1:9000/lab1/Alegre.png'},

#           {
#            'id': 3,
#            'word': 'Intricate',
#            'level': 'B2',
#            'language': 'Английский',
#            'word_class': 'adjective/прилагательное', 
#            'description': 'Something intricate has many complicated details.',
#            'translation': 'сложный, запутанный',
#            'example': 'The watchmaker created an intricate design for the clock.',
#            'synonyms': 'complex, elaborate',
#            'image': 'http://127.0.0.1:9000/lab1/intricate.png'},

#            {
#             'id': 4,
#             'word': 'Resilient',
#             'level': 'C1',
#             'language': 'Английский', 
#             'word_class': 'adjective/прилагательное', 
#             'description': 'Someone who is resilient is able to cope well with difficulties.',
#             'translation': 'устойчивый, стойкий',
#             'example': 'She is a resilient person who has overcome many challenges.',
#             'synonyms': 'adaptable, tenacious',
#             'image': 'http://127.0.0.1:9000/lab1/resilient.png'}]
            
# word_lists = [
#                 {
#                 'id': 1,
#                 'items': [
#                     {
#                     'id': 1,
#                     'word': 'Persistent',
#                     'level': 'C2',
#                     'language': 'Английский',
#                     'word_class': 'adjective/прилагательное',
#                     'description': 'A persistent person continues to do something although other people do not want them to.',
#                     'translation': 'настойчивый, упорный',
#                     'example': 'he was persistent and wouldn\'t leave me alone',
#                     'synonyms': 'determined, perseverant',
#                     'image': 'http://127.0.0.1:9000/lab1/persistent.png'
#                     },
#                     {
#                     'id': 2,
#                     'word': 'Alegre',
#                     'level': 'A1',
#                     'language': 'Испанский',
#                     'word_class': 'adjetivo/прилагательное',
#                     'description': 'Una persona alegre se siente feliz y llena de energía.',
#                     'translation': 'веселый, радостный',
#                     'example': 'Ella siempre está alegre y sonriente.',
#                     'synonyms': 'feliz, contento',
#                     'image': 'http://127.0.0.1:9000/lab1/Alegre.png'
#                     }]},
                
#                 {
#                 'id': 2,
#                 'items': [
#                     {
#                     'id': 3,
#                     'word': 'Intricate',
#                     'level': 'B2',
#                     'language': 'Английский',
#                     'word_class': 'adjective/прилагательное',
#                     'description': 'Something intricate has many complicated details.',
#                     'translation': 'сложный, запутанный',
#                     'example': 'The watchmaker created an intricate design for the clock.',
#                     'synonyms': 'complex, elaborate',
#                     'image': 'http://127.0.0.1:9000/lab1/intricate.png'
#                     },
#                     {
#                     'id': 4,
#                     'word': 'Resilient',
#                     'level': 'C1',
#                     'language': 'Английский',
#                     'word_class': 'adjective/прилагательное',
#                     'description': 'Someone who is resilient is able to cope well with difficulties.',
#                     'translation': 'устойчивый, стойкий',
#                     'example': 'She is a resilient person who has overcome many challenges.',
#                     'synonyms': 'adaptable, tenacious',
#                     'image': 'http://127.0.0.1:9000/lab1/resilient.png'
#                     }]}
#              ]

def GetAllWordCards(words_info):
    try:
      word_list = WordLists.objects.get(status="draft")
      card_count = CardsLists.objects.filter(list=word_list).count()
    except WordLists.DoesNotExist:
      card_count = 0
    searched_word = words_info.GET.get('searched_word', '')  
    found_word_cards = WordCards.objects.filter(word__istartswith=searched_word, status='Active').order_by('id')
    req = WordLists.objects.filter(status='draft').first()
    if searched_word:
        return render(words_info, 'word_cards.html', {'data':  {'word_cards': found_word_cards, 'word_list_id' : req.id if req is not None else 0, 'card_count': card_count}})
    return render(words_info, 'word_cards.html', {'data': {'word_cards': WordCards.objects.filter(status='Active'), 'word_list_id' : req.id if req is not None else 0, 'card_count': card_count}})


def GetWordCard(word_card_info, id):
    return render(word_card_info, 'about_word_card.html', {'data' : WordCards.objects.filter(id = id)[0]})
        

def GetWordLists(word_list_info,id):
    try:
        word_list = WordLists.objects.get(pk=id)
    except WordLists.DoesNotExist:
        req = WordLists.objects.filter(status='draft').first()
        return render(word_list_info, 'word_cards.html', {'data': {'word_cards': WordCards.objects.filter(status='Active'), 'word_list_id' : req.id if req is not None else 0}})
    cards_lists = CardsLists.objects.filter(list=word_list).order_by('lists_order')
    word_cards = []
    for card_list_item in cards_lists:
        # Access the card and order information from the CardsLists object
        card = card_list_item.card
        order = card_list_item.lists_order
        word_cards.append({
            'card': card,
            'order': order
        })
    data = {
        'id': word_list.id,
        'word_cards': word_cards,
        'creation_datetime': word_list.creation_date,
        'week':  word_list.creation_date + timedelta(days=7),
        'month': word_list.creation_date + timedelta(days=30),
        'three_months': word_list.creation_date + timedelta(days=90),
        'order': cards_lists
    }
    return render(word_list_info, 'word_list_card.html', {'data': data})
    

def add_to_list(request):
    if request.method == "POST":
        card_id = request.POST.get('add_button')
        card = WordCards.objects.get(pk=card_id)
        try:
            word_list = WordLists.objects.get(status="draft")
        except WordLists.DoesNotExist:
            word_list = WordLists.objects.create(status="draft", creation_date=timezone.now().date(), learn_until_date=timezone.now().date() + timedelta(days=7))
        existing_cards_count = CardsLists.objects.filter(list=word_list).count()
        order = existing_cards_count + 1
        CardsLists.objects.create(card=card, list=word_list, lists_order=order)
        return GetAllWordCards(request)
    

def delete_word_list(request, id):
    print(id)
    sql = f"update word_lists set status = 'deleted' where id={id}"
    with connection.cursor() as cursor:
        cursor.execute(sql)
    return GetAllWordCards(request)


# def update_word_list(request, word_list_id):
#   word_list = WordLists.objects.get(pk=word_list_id)
#   if request.method == 'POST':
#     learn_until_date = request.POST.get('dates')
#     print(learn_until_date)
#     if learn_until_date:
#         if learn_until_date:
#             if learn_until_date == 'week':  # Handle "Next Week" option
#                 learn_until_date = learn_until_date + timedelta(days=7)
#             elif learn_until_date == 'month':  # Handle "Next Month" option
#                 learn_until_date = learn_until_date + timedelta(days=30)
#             elif learn_until_date == 'three_months':  # Handle "In 3 Months" option
#                 learn_until_date = learn_until_date + timedelta(days=90)
#             sql = f"update word_lists set learn_until_date = {learn_until_date} where id={id}"
#             with connection.cursor() as cursor:
#                 cursor.execute(sql)
#   return render(request, 'word_list.html', {'data': word_list})




