from django.conf import settings
from django.db import models

class Genre(models.Model):
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text

# Create your models here.
class Topic(models.Model):
    text = models.CharField('Description', max_length=500, unique=True)
    ref = models.FileField(upload_to='refs/', null=True, default=None, blank=True)
    url = models.URLField(max_length=200, null=True, default=None, blank=True)  # the link to 
    add_date = models.DateTimeField('date added')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

    def ranking(self):
        vote_list = self.vote_set.all()
        like_list = [v for v in vote_list if v.kind==1]
        dislike_list = [v for v in vote_list if v.kind==2]
        like = len(like_list)
        dislike = len(dislike_list)
        return like-dislike

    def vote_info(self):
        vote_list = self.vote_set.all()
        like_list = [v.user for v in vote_list if v.kind==1]
        dislike_list = [v.user for v in vote_list if v.kind==2]
        talk_list = [v.user for v in vote_list if v.kind==0]
        return talk_list, like_list, dislike_list

    def link(self):
        return '<a href="/topics/%d/">%s</a>'%(self.id, self.text)

class Vote(models.Model):
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
                vlist[0].delete()
                return
        v = Vote(user=user, topic=topic, kind=kind)
        v.save()
        return v
