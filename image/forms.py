# coding=utf-8
from django import forms
from django.core.files.base import ContentFile
from slugify import slugify
from urllib import request

from .models import Image


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'url', 'description')

    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg', 'png']
        # Search string from right to left.
        extension = url.rsplit('.', 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError("Invalid Image File!")
        return url

    def save(self, force_insert=False, force_update=False, commit=True):
        image = super(ImageForm, self).save(commit=False)
        image_url = self.cleaned_data['url']
        # {0} for title, {1} for extension
        image_name = '{0}.{1}'.format(slugify(image.title), image_url.rsplit('.', 1)[1].lower())
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}
        req = request.Request(url=image_url, headers=headers)
        response = request.urlopen(req)
        image.image.save(image_name, ContentFile(response.read()), save=False)
        if commit:
            image.save()
        return image
