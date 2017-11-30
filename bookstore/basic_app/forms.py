from django import forms
from django.contrib.auth.models import User
from basic_app.models import UserProfileInfo,BookCatalogue
from django.forms import ModelForm
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username','email','password')


class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('profile_pic',)

class BookCatalogueForm(forms.ModelForm):
    book_name = forms.CharField()
    class Meta():
        model = BookCatalogue

        fields = ('book_name',)

