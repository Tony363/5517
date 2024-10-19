from django import forms
from .models import Document
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('upload',)

class UploadFileForm(forms.Form):
    file = forms.FileField()  # You can add validators and labels if needed


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
