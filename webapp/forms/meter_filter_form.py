from django import forms


class MeterFilterForm(forms.Form):
    from_date = forms.CharField(max_length=24)
    to_date = forms.CharField(max_length=24)
