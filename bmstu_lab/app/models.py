from django.db import models

# Create your models here.

class WordLists(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=10)
    creation_date = models.DateField(blank=True, null=True)
    submition_date = models.DateField(blank=True, null=True)
    completion_date = models.DateField(blank=True, null=True)
    creator = models.IntegerField(blank=True, null=True)
    moderator = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'word_lists'


class WordCards(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=10)
    word = models.CharField(max_length=30)
    word_level = models.CharField(max_length=5)
    word_language = models.CharField(max_length=30)
    word_class = models.CharField(max_length=30)
    word_description = models.TextField(blank=True, null=True)
    word_translation = models.CharField(max_length=255)
    word_example = models.TextField(blank=True, null=True)
    word_synonyms = models.CharField(max_length=255, blank=True, null=True)
    word_image = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'word_cards'


class CardsLists(models.Model):
    id = models.AutoField(primary_key=True)
    card = models.ForeignKey('WordCards', models.SET_NULL, blank=True, null=True)
    list = models.ForeignKey('WordLists', models.SET_NULL, blank=True, null=True)
    lists_order = models.IntegerField(blank=True, null=True, default=1)

    class Meta:
        managed = False
        db_table = 'cards_lists'
