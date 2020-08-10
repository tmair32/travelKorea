from django import forms
from .models import Score, Comment

class ScoreForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = ['score', 'content', ]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', ]