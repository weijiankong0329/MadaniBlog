from django import forms

class BlogSearchForm(forms.Form):
    search_term = forms.CharField(label='Search')