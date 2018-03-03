from django.contrib import admin
from .models import Topic, Vote, Genre

# Register your models here.
admin.site.register(Genre)
admin.site.register(Topic)
admin.site.register(Vote)
