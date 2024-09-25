from django.shortcuts import render
from django.http import HttpResponse




word_cards = [{
          'id' : 1, 
          'word': 'Persistent', 
          'level' : 'C2',
          'language' : 'Английский',
          'word_class' : 'adjective/прилагательное', 
          'description': 'A persistent person continues to do something although other people do not want them to.', 
          'translation': 'настойчивый, упорный', 
          'example' : "he was persistent and wouldn't leave me alone", 
          'synonyms' : 'determined, perseverant', 
          'image' : 'http://127.0.0.1:9000/lab1/persistent.png'},

         {
          'id': 2,
          'word': 'Alegre',
          'level': 'A1',
          'language': 'Испанский', 
          'word_class': 'adjetivo/прилагательное', 
          'description': 'Una persona alegre se siente feliz y llena de energía.',
          'translation': 'веселый, радостный',
          'example': 'Ella siempre está alegre y sonriente.',
          'synonyms': 'feliz, contento',
          'image': 'http://127.0.0.1:9000/lab1/Alegre.png'},

          {
           'id': 3,
           'word': 'Intricate',
           'level': 'B2',
           'language': 'Английский',
           'word_class': 'adjective/прилагательное', 
           'description': 'Something intricate has many complicated details.',
           'translation': 'сложный, запутанный',
           'example': 'The watchmaker created an intricate design for the clock.',
           'synonyms': 'complex, elaborate',
           'image': 'http://127.0.0.1:9000/lab1/intricate.png'},

           {
            'id': 4,
            'word': 'Resilient',
            'level': 'C1',
            'language': 'Английский', 
            'word_class': 'adjective/прилагательное', 
            'description': 'Someone who is resilient is able to cope well with difficulties.',
            'translation': 'устойчивый, стойкий',
            'example': 'She is a resilient person who has overcome many challenges.',
            'synonyms': 'adaptable, tenacious',
            'image': 'http://127.0.0.1:9000/lab1/resilient.png'}]
            
word_lists = [
                {
                'id': 1,
                'items': [
                    {
                    'id': 1,
                    'word': 'Persistent',
                    'level': 'C2',
                    'language': 'Английский',
                    'word_class': 'adjective/прилагательное',
                    'description': 'A persistent person continues to do something although other people do not want them to.',
                    'translation': 'настойчивый, упорный',
                    'example': 'he was persistent and wouldn\'t leave me alone',
                    'synonyms': 'determined, perseverant',
                    'image': 'http://127.0.0.1:9000/lab1/persistent.png'
                    },
                    {
                    'id': 2,
                    'word': 'Alegre',
                    'level': 'A1',
                    'language': 'Испанский',
                    'word_class': 'adjetivo/прилагательное',
                    'description': 'Una persona alegre se siente feliz y llena de energía.',
                    'translation': 'веселый, радостный',
                    'example': 'Ella siempre está alegre y sonriente.',
                    'synonyms': 'feliz, contento',
                    'image': 'http://127.0.0.1:9000/lab1/Alegre.png'
                    }]},
                
                {
                'id': 2,
                'items': [
                    {
                    'id': 3,
                    'word': 'Intricate',
                    'level': 'B2',
                    'language': 'Английский',
                    'word_class': 'adjective/прилагательное',
                    'description': 'Something intricate has many complicated details.',
                    'translation': 'сложный, запутанный',
                    'example': 'The watchmaker created an intricate design for the clock.',
                    'synonyms': 'complex, elaborate',
                    'image': 'http://127.0.0.1:9000/lab1/intricate.png'
                    },
                    {
                    'id': 4,
                    'word': 'Resilient',
                    'level': 'C1',
                    'language': 'Английский',
                    'word_class': 'adjective/прилагательное',
                    'description': 'Someone who is resilient is able to cope well with difficulties.',
                    'translation': 'устойчивый, стойкий',
                    'example': 'She is a resilient person who has overcome many challenges.',
                    'synonyms': 'adaptable, tenacious',
                    'image': 'http://127.0.0.1:9000/lab1/resilient.png'
                    }]}
             ]

def GetAllWordCards(words_info):
    searched_word = words_info.GET.get('searched_word')  # Get the query from GET parameters
    found_words = []
    if searched_word:
        found_words = [word for word in word_cards if searched_word.lower() in word['word'].lower()]
        return render(words_info, 'word_cards.html', {'data': {'word_cards': found_words}})
    return render(words_info, 'word_cards.html', {'data': {'word_cards': word_cards}})


def GetWordCard(word_card_info, id):
    for word in word_cards:
        if word['id'] == id:
            return render(word_card_info, 'about_word_card.html', {'data' : word})
        
def GetWordLists(word_list_info,id):
    for word_list in word_lists:
        if word_list['id'] == id:
            return render(word_list_info, 'word_list_card.html', {'data' : word_list['items']})



