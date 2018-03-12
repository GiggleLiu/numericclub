from django.db import models
from django.contrib.auth.models import Permission, PermissionsMixin
from django.core.mail import send_mail
from django.contrib.contenttypes.models import ContentType
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from numericclub.settings import THUMB_SIZE   
import os.path

from django.contrib.auth.base_user import AbstractBaseUser
from .managers import UserManager

class AdvancedUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    truename = models.CharField(max_length=64)
    credit = models.IntegerField(default=0)
    avatar = models.ImageField(upload_to='avatars', null=True, blank=True)
    thumbnail = models.ImageField(upload_to='avatar_thumbs', editable=False, null=True, blank=True)

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
        return '<a href="/being/%d/">%s</a>'%(self.id, self.truename)

    def interest(self):
        interest_list = []
        for vote in self.vote_set.all():
            if vote.kind == 1:
                interest_list.append(vote.topic)
        return interest_list

    def save(self, *args, **kwargs):
        try:
            self.make_thumbnail()
        except:
            # set to a default thumbnail
            print('Could not create thumbnail - is the file type valid?')
        super(AdvancedUser, self).save(*args, **kwargs)

    def make_thumbnail(self):
        image = Image.open(self.avatar)
        image.thumbnail(THUMB_SIZE, Image.ANTIALIAS)

        thumb_name, thumb_extension = os.path.splitext(self.avatar.name)
        thumb_extension = thumb_extension.lower()

        thumb_filename = thumb_name + '_thumb' + thumb_extension

        if thumb_extension in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif thumb_extension == '.gif':
            FTYPE = 'GIF'
        elif thumb_extension == '.png':
            FTYPE = 'PNG'
        else:
            return False    # Unrecognized file type

        # Save thumbnail to in-memory file as BytesIO
        temp_thumb = BytesIO()
        image.save(temp_thumb, FTYPE)
        temp_thumb.seek(0)

        # set save=False, otherwise it will run in an infinite loop
        self.thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
        temp_thumb.close()

        return True

def getuserbyname(name):
    try:
        user = AdvancedUser.objects.get(truename=name)
        return user
    except:
        return None

def getadmin():
    return AdvancedUser.objects.get(email='aadddss@sina.com')

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

