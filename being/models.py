#-*-coding:utf-8-*-
from django.db import models
from django.contrib.auth.models import Permission, PermissionsMixin
from django.core.mail import send_mail
from django.contrib.contenttypes.models import ContentType

from django.contrib.auth.base_user import AbstractBaseUser
from .managers import UserManager

class AdvancedUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    truename = models.CharField(max_length=64)
    credit = models.IntegerField(default=0)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    description = models.CharField(null=True, blank=True, max_length=512)
    is_admin = models.BooleanField(default=False)

    is_staff = models.BooleanField(
        'staff status',
        default=False,
        help_text='Designates whether the user can log into this admin site.',
    )
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    EMAIL_FIELD = 'email'

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return '%s' % (self.truename)

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def link(self):
        return '<a href="/being/user_detail/%d/">%s</a>'%(self.id, self.truename)

def getuserbyname(name):
    try:
        user = AdvancedUser.objects.get(truename=name)
        return user
    except:
        return None

def getadmin():
    return getuserbyname('cacate')

def newuser(truename, password, email, description, avatar):
    user = AdvancedUser(truename=truename, email=email, description=description, avatar=avatar)
    user.set_password(password)
    user.save()
    return user

def updateuser(user, description, avatar):
    if avatar:
        user.avatar = avatar
    user.description = description
    user.save()

def updatepassword(user, oldpassword, newpassword):
    if user.check_password(oldpassword):
        user.set_password(newpassword)
        user.save()

