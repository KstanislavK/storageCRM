from django import forms

from .models import PartnersList


class PartnersForm(forms.ModelForm):
    class Meta:
        model = PartnersList
        exclude = ('is_active', )
