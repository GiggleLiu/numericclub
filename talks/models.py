from django.conf import settings
from django.db import models
from datetime import datetime

from topics.models import Topic

class Talk(models.Model):
    title = models.CharField(max_length=200, unique=True)
    md_file = models.FileField(upload_to='announcements/', null=True, default=None, blank=True)
    github_url = models.URLField(max_length=200, null=True, default=None, blank=True)  # the link to 
    add_date = models.DateTimeField('date added')
    talk_date = models.DateTimeField('talk date')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

def get_current_talk():
    try:
        t = Talk.objects.latest('talk_date')
        if t.talk_date>datetime.now(t.talk_date.tzinfo):
            return t
    except:
        pass

# TODO: payments
