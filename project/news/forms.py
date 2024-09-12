from django import forms
from .models import Post
from django.core.exceptions import ValidationError


class PostForm(forms.ModelForm):
   class Meta:
      model = Post
      fields = [
         'author',
         'choise',
         'category',
         'title',
         'text',
         'category',
         'reting',
      ]

   def clean(self):
      cleaned_data = super().clean()
      text = cleaned_data.get("text")
      title = cleaned_data.get("title")

      if title == text:
         raise ValidationError(
            "Заголовок не должен быть идентичен тексту."
         )

      return cleaned_data
