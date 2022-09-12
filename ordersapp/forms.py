from django import forms

from .models import OrderList, OrderProductsList


class SearchForm(forms.Form):
    pass


class NewOrderForm(forms.ModelForm):
    class Meta:
        model = OrderList
        exclude = ('created', 'user_creator', 'shipped', 'shipped_date')
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 2, 'cols': 30}),
        }


class UpdateOrderForm(forms.ModelForm):
    class Meta:
        model = OrderList
        exclude = ('created_at', 'shipped_date')
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 2, 'cols': 30}),
        }


class OrderProductForm(forms.ModelForm):
    class Meta:
        model = OrderProductsList
        exclude = ('order',)


class OrderProductUpdateForm(forms.ModelForm):

    class Meta:
        model = OrderProductsList
        exclude = ('order',)
        # widgets = {
        #     'batch': forms.Select()
        # }

