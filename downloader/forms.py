from django import forms

class YouTubeURLForm(forms.Form):
    url = forms.URLField(label='YouTube URL', max_length=200)
