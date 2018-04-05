from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.cache import cache
from numericclub.utils import get_readme_html
if "mailer" in settings.INSTALLED_APPS:
    from mailer import send_mail
else:
    from django.core.mail import send_mail

from topics.models import Topic
from being.models import getadmin, AdvancedUser

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


    def inform(self, user_list=None):
        '''
        send email to user list.
        '''
        if user_list is None:
            user_list = AdvancedUser.objects.all()
        title = 'Numeric Club - New Talk: %s'%self.title

        for user in user_list:
            msg = '''Dear %s:

We have a new talk ready,

Title:       %s
On Topic:    %s
Github Link: %s
Date Time:   %s
Speaker:     %s
Location:    %s

Welcome for your paticipation, and don't forget to bring your laptops!

Yours,
Numeric Club
'''%(user.truename, self.title, self.topic.text, self.github_url, self.talk_date, self.user.truename, self.location)

            #email = EmailMessage(title, msg, to=[user.email])
            #email.send()
            print('sending %s'%user.email, msg)

            send_mail(title, msg,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
            )

# TODO: payments

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

def headercontent4talk(talk, reload=False):
    cache_id = 'headercontent-talk-%d'%talk.id
    res = cache.get(cache_id)
    if res is None or reload:
        res = get_readme_html(talk.github_url)
        cache.set(cache_id, res, 600)
    return res
