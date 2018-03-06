from django.conf import settings
from django.db import models
from django.utils import timezone

from topics.models import Topic
from being.models import getadmin

class Talk(models.Model):
    class Meta:
        ordering=['-talk_date']

    title = models.CharField(max_length=200, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET(getadmin))
    md_file = models.FileField(upload_to='announcements/', null=True, default=None, blank=True)
    github_url = models.URLField(max_length=200, null=True, default=None, blank=True)  # the link to 
    add_date = models.DateTimeField('date added')
    talk_date = models.DateTimeField('time')
    location = models.CharField(max_length=200, default=u'北京海淀区中科院物理所M楼830对面玻璃房(Opposite to Room 830 Building M, IOP CAS, BeiJing)')
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    KIND_CHOICES = ((0, 'preparing'), (1, 'ready'), (2, 'finished'), (3, 'disqualified'))
    status = models.IntegerField(choices=KIND_CHOICES, default=0)

    def __str__(self):
        return self.title

    def link(self):
        return '<a href="/talks/%d/">%s</a>'%(self.id, self.title)


def get_current_talk():
    ready = Talk.objects.filter(status=1)
    if len(ready) > 0:
        t = ready.earliest('talk_date')
        if t.talk_date<timezone.now():
            t.status = 2
            t.save()
            return get_current_talk()
        else:
            return t
    else:
        finished = Talk.objects.filter(status=2)
        if len(finished) > 0:
            t = finished.latest('talk_date')
            return t
        else:
            return None

# TODO: payments
