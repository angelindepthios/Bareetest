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

    def clean_rating(self):
        rating = self.cleaned_data.get("rating")
        if not rating:
            raise forms.ValidationError("Rating is required.")
        return rating

    def clean_comment(self):
        comment = self.cleaned_data.get("comment", "").strip()
        if not comment:
            raise forms.ValidationError("Comment cannot be empty.")
        return comment