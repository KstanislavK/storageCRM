from django import forms

from ordersapp.models import TKList
from .models import ProductList, NomenList, BatchList, CategoryList


class ProductForm(forms.ModelForm):
    class Meta:
        model = ProductList
        exclude = ('slug', 'is_active', 'name')


class TkCreateViewForm(forms.ModelForm):
    class Meta:
        model = TKList
        exclude = ('pk', )

    def __init__(self, *args, **kwargs):
        super(TkCreateViewForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class BatchCreateViewForm(forms.ModelForm):
    class Meta:
        model = BatchList
        exclude = ('slug', )

    def __init__(self, *args, **kwargs):
        super(BatchCreateViewForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class CategoryCreateViewForm(forms.ModelForm):
    class Meta:
        model = CategoryList
        exclude = ('slug', )

    def __init__(self, *args, **kwargs):
        super(CategoryCreateViewForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class NomenForm(forms.ModelForm):
    class Meta:
        model = NomenList
        exclude = ('slug', 'is_active')

    def __init__(self, *args, **kwargs):
        super(NomenForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class SearchForm(forms.Form):
    pass
