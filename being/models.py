#-*-coding:utf-8-*-
from django.db import models
from django.contrib.auth.models import Group, Permission, PermissionsMixin
from django.core.mail import send_mail
from django.contrib.contenttypes.models import ContentType

from django.contrib.auth.base_user import AbstractBaseUser
from .managers import UserManager

class AdvancedUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=64)
    credit = models.IntegerField(default=0)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    description = models.CharField(null=True, blank=True, max_length=512)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return '%s' % (self.username)

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def link(self):
        return '<a href="/being/user_detail/%d/">%s</a>'%(self.user.id, self.truename)

def getuserbyname(name):
    try:
        user = AdvancedUser.objects.get(username=name)
        return user
    except:
        return None

def getadmin():
    return getuserbyname('cacate')

def newuser(username, password, email, description, avatar):
    user = AdvancedUser(username=username, email=email, description=description, avatar=avatar)
    user.set_password(password)
    g = Group.objects.get(name='default')
    user.save()
    user.groups.add(g)
    return user

def updateuser(user, oldpassword, newpassword, email, description, avatar):
    if user.check_password(oldpassword):
        user.email = email
        user.set_password(newpassword)
        if avatar:
            user.avatar = avatar
        user.description = description
        user.save()

