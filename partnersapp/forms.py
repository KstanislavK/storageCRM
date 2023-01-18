from django import forms

from .models import PartnersList


class PartnersForm(forms.ModelForm):
    class Meta:
        model = PartnersList
        exclude = ('is_active', 'slug')

    def __init__(self, *args, **kwargs):
        super(PartnersForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
