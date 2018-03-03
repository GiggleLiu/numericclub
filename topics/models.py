from django.conf import settings
from django.db import models

class Genre(models.Model):
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text

# Create your models here.
class Topic(models.Model):
    text = models.CharField(max_length=500, unique=True)
    ref = models.FileField(upload_to='refs/', null=True, default=None, blank=True)
    url = models.URLField(max_length=200, null=True, default=None, blank=True)  # the link to 
    add_date = models.DateTimeField('date added')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

    def ranking(self):
        return sum([v.kind for v in self.vote_set.all()])

class Vote(models.Model):
    '''
    kind:
        1: user like topic
        -1: user dislike topic
        0: user like to give a talk
    '''
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    kind = models.IntegerField(default=0)

def get_topics_ranked(genre):
    topics = genre.topic_set.all()
    sorted(topics, key=lambda t:-t.ranking())
    return topics
