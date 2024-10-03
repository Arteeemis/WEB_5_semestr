from django.shortcuts import render
from django.http import HttpResponse
from app.models import WordLists, WordCards, CardsLists
from django.db.models import Q, F
from django.core.exceptions import BadRequest
from datetime import date
from django.db import connection
import psycopg2


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
    searched_word = words_info.GET.get('searched_word', '')  # Get the query from GET parameters
    found_word_cards = WordCards.objects.filter(word__istartswith=searched_word, status='Active').order_by('id')
    req = WordLists.objects.filter(status='draft').first()
    if searched_word:
        return render(words_info, 'word_cards.html', {'data':  {'word_cards': found_word_cards, 'word_list_id' : req.id if req is not None else 0}})
    return render(words_info, 'word_cards.html', {'data': {'word_cards': WordCards.objects.filter(status='Active'), 'word_list_id' : req.id if req is not None else 0}})


def GetWordCard(word_card_info, id):
    return render(word_card_info, 'about_word_card.html', {'data' : WordCards.objects.filter(id = id)[0]})
        

def GetWordLists(word_list_info,id):
    data = get_word_list_data(id)
    return render(word_list_info, 'word_list_card.html', {'data' : {'id': data['id'], 'word_cards' : data['data'], 'creation_datetime' : data['creation_datetime'] }})




def get_word_list_data(word_list_id):
    req = WordLists.objects.filter(~Q(status='deleted'),id=word_list_id).first()
    if req is None:
        raise BadRequest('Invalid Request')
    # Use CardsLists to filter WordCards based on the word_list_id
    content = WordCards.objects.filter(
        cardslists__list=req
    ).annotate(
        order=F('cardslists__lists_order'),  # Access lists_order through CardsLists
        creation_date=F('cardslists__list__creation_date')  # Access creation_date through WordLists
    ).order_by('cardslists__lists_order')  # Ensure order is respected

    # Fetch the creation_date (no need to do it for each object)
    creation_date = req.creation_date 

    return {
        'id': word_list_id,
        'data': content,
        'creation_datetime': creation_date
    }



def get_or_create_word_list():
    req = WordLists.objects.filter(status='draft').first()
    if req is None:
        word_list = WordLists(status='draft', creation_date=date.today())
        word_list.save()
        print(word_list.id)
        return word_list.id
    print(req.id)
    return req.id


def add_word_card_to_list(request):
    data = request.POST
    card_id = data.get("add_button")
    word_list_id = get_or_create_word_list()  # Assuming this function exists

    # Create a new CardsLists entry to connect the card and list
    card_list = CardsLists.objects.filter(
        card_id=card_id,
        list_id=word_list_id
    ).first()

    if not card_list:
        # Create a new CardsLists object
        card_list = CardsLists(
            card_id=card_id,
            list_id=word_list_id,
            lists_order=1
        )
        card_list.save()

    return GetAllWordCards(request)  


def delete_word_list(request, id):
    print(id)
    sql = f"update word_lists set status = 'deleted' where id={id}"
    with connection.cursor() as cursor:
        cursor.execute(sql)
    return GetAllWordCards(request)
