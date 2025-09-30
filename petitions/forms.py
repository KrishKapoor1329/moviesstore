from django import forms
from .models import Petition

class PetitionForm(forms.ModelForm):
    class Meta:
        model = Petition
        fields = ['title', 'description', 'movie_year', 'director', 'genre', 'imdb_link']
        widgets = {
            'title':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter movie title'}),
            'description':forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Explain why this movie should be added'}),
            'movie_year':forms.NumberInput(attrs={'class': 'form-control'}),
            'director':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Director name optional'}),
            'genre':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Genre optional'}),
            'imdb_link':forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://www.imdb.com/title/...'}),
        }