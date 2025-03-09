from .models import OpeningHour
from django import forms


class OpeningHourForm(forms.ModelForm):
    class Meta:
        model = OpeningHour
        fields = ["day", "from_hour", "to_hour", "is_closed"]
