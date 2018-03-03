#-*-coding:utf-8-*-
from django.db import models
from django.contrib.auth.models import User, Group, Permission
from django.core.mail import send_mail
from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError
from django.db.models import Q
import datetime
import re

# Create your models here.


class Being(models.Model):
    '''define the basic person model'''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    truename = models.CharField(max_length=64)
    description = models.CharField(null=True, blank=True, max_length=512)
    avatar = models.ImageField(upload_to='avatar/', blank=True, null=True)
    credit = models.IntegerField(default=0)

    class Meta:
        ordering = ['truename']

    def __unicode__(self):
        return '%s' % (self.truename)

    def link(self):
        return '<a href="/being/user_detail/' + str(self.user.id) + '/">' + self.truename + '</a>'

def getuser(uid):
    return User.objects.get(id=uid)


def getbeing(bid):
    return Being.objects.get(id=bid)


def getbeingbyuser(user):
    return Being.objects.get(user=user)


def getbeingbyname(name):
    user = User.objects.get(username=name)
    return Being.objects.get(user=user)


def getuserbyname(name):
    try:
        user = User.objects.get(username=name)
        return user
    except:
        return None


def getrecordlist(user):
    pass
    # l=list(user.clauserecord_set.all())
    # l=l+list(user.creaturerecord_set.all())
    # l=l+list(user.postrecord_set.all())
    #l.sort(key=lambda x:x.happentime,reverse=True)
    # return l


def mailcall(user):
    send_mail('遥远星球的呼叫', '有人在星球上呼叫了您，这是一封邮件提醒~',
              from_email='postmaster@yanglala.com', recipient_list=[user.email])
    return True


def getadmin():
    return getuserbyname('cacate')


def getgroupuser():
    return getuserbyname('group')


def newbeing(user, truename, description, avatar):
    if truename is None:
        truename = user.username
    being = Being(user=user, truename=truename,
                  description=description, avatar=avatar)
    being.save()
    return being


def newuser(username, password, email):
    user = User(username=username, email=email)
    user.set_password(password)
    g = Group.objects.get(name='default')
    user.save()
    user.groups.add(g)
    return user


def deleteuser(uid):
    User.objects.get(pk=uid).delete()
    return True


def updateuser(user, oldpassword, newpassword, email):
    if user.check_password(oldpassword):
        user.email = email
        user.set_password(newpassword)
        user.save()


def updatebeing(user, truename, description, avatar):
    being = Being.objects.get(user=user)
    being.truename = truename
    being.description = description
    if avatar:
        being.avatar = avatar
    being.save()
    return being


def getperm(perm):
    try:
        pm = Permission.objects.get(codename=perm)
        return pm
    except:
        return False


def newperm(perm):
    content_type = ContentType.objects.get(app_label='being', model='being')
    pminner = Permission.objects.create(
        codename=perm, name=perm, content_type=content_type)
    return pminner


def addpermtouser(user, perm):
    getperm(perm)
    user.user_permissions.add(pminner)
    return True


def addpermtogroup(group, perm):
    pminner = getperm(perm)
    group.permissions.add(pminner)
    return True


def getgroup(gname):
    try:
        g = Group.objects.get(name=gname)
        return g
    except:
        return None


def newgroup(gname):
    g = Group(name=gname)
    g.save()
    return g


def ghas_perm(group, perm):
    return group.permissions.filter(codename=perm)


def getmemberlist():
    gs = set(getgroup('student').user_set.all())
    gp = set(getgroup('professor').user_set.all())
    gs.update(gp)
    ulist = [user for user in gs if hasattr(user, 'being')]
    blist = [user.being for user in ulist]
    return blist
