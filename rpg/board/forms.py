from tinymce.widgets import TinyMCE
from django import forms
from .models import Advertisement, Response, Category

class AdvertisementForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE())

    class Meta:
        model = Advertisement
        fields = ['title', 'content', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Заголовок объявления'}),
            'category': forms.Select(),
        }
        labels = {
            'title': '',
            'content': '',
            'category': '',
        }

class ResponseForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Напишите комментарий...'}), label='')

    class Meta:
        model = Response
        fields = ['content']
        

