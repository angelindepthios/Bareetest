from django import forms
from .models import RatingComment

class RatingCommentForm(forms.ModelForm):
    class Meta:
        model = RatingComment
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.RadioSelect(choices=RatingComment.RATING_CHOICES),
            'comment': forms.Textarea(attrs={'class': 'w-full p-2 border rounded-md', 'rows': 3}),
        }
