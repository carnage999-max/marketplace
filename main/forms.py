from django import forms
from .models import *
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import PasswordChangeForm


class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'first_name',
            'last_name', 'phone_number',
            'state', 'lga',
            'gender', 'password1', 'password2'
        ]


class UpdateProfileForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'gender', 'phone_number', 'state', 'lga',
            'shop_description', 'shop_url',
            'facebook', 'x_twitter', 'instagram', 'linkedin'
        ]


class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control'})


class SignInForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class AddProductForm(ModelForm):
    class Meta:
        model = Product
        fields = [
            'product_name', 'product_description', 'product_image', 'price',
            'quantity', 'category', 'sub_category'
        ]
        widgets = {
            'product_image': forms.ClearableFileInput(attrs={'multiple':True})
        }


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['comment']


class ReplyForm(ModelForm):
    class Meta:
        model = Reply
        fields = ['comment']


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    phone_number = forms.IntegerField()
    subject = forms.CharField(max_length=200, required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)


class ReportForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    phone_number = forms.IntegerField()
    subject = forms.CharField(max_length=200, required=True)
    issue = forms.CharField(widget=forms.Textarea, required=True)


class MessageForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows':4, 'placeholder': 'Write your Message...'}))

