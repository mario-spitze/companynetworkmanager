from django import forms
from .models import Workplace, Customer

class HandoverForm(forms.Form):
    workplace = forms.ModelChoiceField(label='an Arbeitsplatz', initial=-1, queryset=Workplace.objects.all(), required=False)
    customer = forms.ModelChoiceField(label='an Person', initial=-1, queryset=Customer.objects.all(), required=False)