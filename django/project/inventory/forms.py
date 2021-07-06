from django import forms
from .models import Article, HardwareClass, Workplace, Customer

class HandoverForm(forms.Form):
    workplace = forms.ModelChoiceField(label='an Arbeitsplatz', initial=-1, queryset=Workplace.objects.all(), required=False)
    customer = forms.ModelChoiceField(label='an Person', initial=-1, queryset=Customer.objects.all(), required=False)

ArticleType =(
    ("i", "individual"),
    ("b", "bulk"),
)

class ArticleCreateForm(forms.Form):

    type = forms.ChoiceField(label='Type', choices=ArticleType)
    name = forms.CharField(label="Name")
    ean = forms.IntegerField(label="EAN", required=False)
    hardwareClass = forms.ModelChoiceField(label="Kategorie", queryset=HardwareClass.objects.all())
