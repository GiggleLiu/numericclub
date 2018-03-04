from django import forms

from .models import Topic

class NewTopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'rows': '4'}),
        }

class UpdateTopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'rows': '4'}),
        }

