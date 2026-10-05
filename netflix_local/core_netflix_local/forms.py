from django.forms import ModelForm
from .models import ViewerProfile
from django import forms

class ViewerProfileForm(ModelForm):
    class Meta:
        model = ViewerProfile
        fields = ["name", "age", "user"]

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        if "$" in name or "@" in name:
            self.add_error('name', "Special Characters not allowed.")
        return cleaned_data
