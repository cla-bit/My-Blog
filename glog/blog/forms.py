from django import forms
from .models import Comment


class EmailShareForm(forms.Form):
    name = forms.CharField(max_length=30, min_length=3, required=True, label="Your Name")
    send_to = forms.EmailField(label="Your Email")
    to_receiver = forms.EmailField(label="To Who")
    comments = forms.CharField(required=False, label="Comment here....", widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model= Comment
        fields = ['user_img', 'name', 'email', 'body']

