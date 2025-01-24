from django import forms
from .models import Rating, Comment

class RatingCommentForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ["rating"]
        labels = {"rating": "Rating"}
        help_texts = {"rating": "Rate this product from 1 to 5 stars."}