# Dans forms.py
from django import forms
from .models import Performance


class PerformanceForm(forms.ModelForm):
    class Meta:
        model = Performance
        fields = '__all__'  # Ou spécifiez les champs que vous voulez afficher dans le formulaire
