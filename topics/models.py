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
        like = len([v for v in self.vote_set.all() if v.kind==1])
        dislike = len([v for v in self.vote_set.all() if v.kind==2])
        return like-dislike

    def link(self):
        return '<a href="/topics/detail/%d/">%s</a>'%(self.id, self.text)

class Vote(models.Model):
    '''
    kind:
        1: user like topic
        2: user dislike topic
        0: user like to give a talk
    '''
    KIND_CHOICES = ((0, 'can talk'), (1, 'like'), (2,'dislike'))
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    kind = models.IntegerField(choices=KIND_CHOICES)

def get_topics_ranked(genre):
    topics = genre.topic_set.all()
    sorted(topics, key=lambda t:-t.ranking())
    return topics

def newvote(user, topic, kind):
    vlist = Vote.objects.filter(user=user, topic=topic, kind=kind)
    if len(vlist) != 0:
        if kind==0:
            vlist[0].delete()
        return
    else:
        if kind!=0:
            print(kind)
            vlist = Vote.objects.filter(user=user, topic=topic, kind=3-kind)
            if len(vlist)!=0:
                print('@@@@@')
                vlist[0].delete()
                return
        v = Vote(user=user, topic=topic, kind=kind)
        v.save()
        return v
