from django import forms

from .models import RideList, MileageList


class SearchForm(forms.Form):
    pass


class NewRideForm(forms.ModelForm):
    class Meta:
        model = RideList
        exclude = ('order', 'created_at', 'delivered', 'delivered_at')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2, 'cols': 30}),
        }


class NewMileageForm(forms.ModelForm):
    class Meta:
        model = MileageList
        exclude = ('km_start', 'consumption', 'km_amount')

    def __init__(self, *args, **kwargs):
        super(NewMileageForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
