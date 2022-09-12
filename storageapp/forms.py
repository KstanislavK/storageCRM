from django import forms

from .models import ProductList, NomenList


class ProductForm(forms.ModelForm):
    class Meta:
        model = ProductList
        exclude = ('slug', 'is_active', 'name')


class NomenForm(forms.ModelForm):
    class Meta:
        model = NomenList
        exclude = ('slug', 'is_active')


class SearchForm(forms.Form):
    pass
