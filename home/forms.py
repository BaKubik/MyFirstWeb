from django import forms
from django.contrib.auth.models import User

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)

    def send_mail(self):
        pass


class UserForm(forms.ModelForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


    class Meta:
        model = User
        fields = ['username', 'email', 'password']


