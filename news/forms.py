from django import forms
from .models import Category, News
import re
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField


# Форма не связаная с моделью
# class NewsForm(forms.Form):
#     title = forms.CharField(max_length=150, label="Заголовок", widget=forms.TextInput(attrs={'class': 'form-control'}))
#     content = forms.CharField(label="Текст", required=False, widget=forms.Textarea(attrs={
#         'class': 'form-control',
#         'rows': 5
#     }))
#     is_published = forms.BooleanField(label="Опубликовано?", initial=True)
#     category = forms.ModelChoiceField(empty_label="Выберите категорию", label="Категория",
#                                       queryset=Category.objects.all(),
#                                       widget=forms.Select(attrs={'class': 'form-control'}))


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=150, label="Тема письма",
                              widget=forms.TextInput(attrs={'class': 'form-control'}))
    text = forms.CharField(max_length=150, label="Текст",
                           widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    captcha = CaptchaField()


# Форма связаная с моделью
class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        # fields = "__all__"
        fields = ['title', 'content', 'is_published', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'category': forms.Select(attrs={'class': 'form-control'})
        }

    # Кастомный валидатор
    def clean_file(self):
        title = self.cleaned_data['title']
        if re.match(r'\d', title):
            raise ValidationError('Название не должно начинаться с цифры')
        return title
