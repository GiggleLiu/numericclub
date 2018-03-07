from django import forms
from django.contrib.admin import widgets
from bootstrap3_datetime.widgets import DateTimePicker

from .models import Talk

class NewTalkForm(forms.ModelForm):
    class Meta:
        model = Talk
        fields = ('title', 'talk_date', 'github_url')
        widgets = {
                'talk_date': DateTimePicker(options={"format": "YYYY-MM-DD HH:mm",
                                                           }),
                }

class UpdateTalkForm(forms.ModelForm):
    class Meta:
        model = Talk
        fields = ('title', 'talk_date', 'github_url', 'location')
        widgets = {
                'talk_date': DateTimePicker(options={"format": "YYYY-MM-DD HH:mm",
                                                           }),
                }
