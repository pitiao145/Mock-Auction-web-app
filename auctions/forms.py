from django import forms
from .models import CATEGORIES

class CreateListingForm(forms.Form):
    title = forms.CharField(label="Title", max_length=64)
    description = forms.CharField(widget=forms.Textarea, label="Description")
    start = forms.CharField(label="Starting bid", widget=forms.NumberInput)
    imgUrl = forms.CharField(label="Image URL", required=False)
    category = forms.ChoiceField(label="Category", choices=CATEGORIES, widget=forms.Select(attrs={
        "selected": "Choose a category",
    }))

