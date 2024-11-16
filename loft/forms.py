from django import forms
from .models import Category, Profile, Customer, Shipping
from django_svg_image_form_field import SvgAndImageFormField
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth.models import User


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = []
        field_classes = {
            'icon': SvgAndImageFormField,
        }


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control contact__section-input'
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control contact__section-input'
    }))


class RegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control contact__section-input'
    }))

    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control contact__section-input'
    }))

    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control contact__section-input'
    }))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control contact__section-input'
    }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control contact__section-input',
    }))

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control contact__section-input'
    }))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2', 'email')


class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone']
        widgets = {
            'phone': forms.TextInput(attrs={
                'class': 'form-control contact__section-input'
            })
        }


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя получателя'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Фамилия получателя'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email получателя'
            }),

        }


class ShippingForm(forms.ModelForm):
    class Meta:
        model = Shipping
        fields = ['phone', 'city', 'address', 'first_name', 'last_name', 'comment']
        widgets = {
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 4px; margin-top: 5px;'
            }),

            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 4px; margin-top: 5px;'
            }),

            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 4px; margin-top: 5px;'
            }),

            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 4px; margin-top: 5px;'
            }),

            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 4px; margin-top: 5px;'
            }),

            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 4px; margin-top: 5px;'
            }),
        }


class ChangeAccountForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control contact__section-input'
            }),

            'last_name': forms.TextInput(attrs={
                'class': 'form-control contact__section-input'
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control contact__section-input'
            }),
        }


class ChangeProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'city', 'street', 'house', 'flat']
        widgets = {
            'phone': forms.TextInput(attrs={
                'class': 'form-control contact__section-input'
            }),

            'city': forms.TextInput(attrs={
                'class': 'form-control contact__section-input'
            }),

            'street': forms.TextInput(attrs={
                'class': 'form-control contact__section-input'
            }),

            'house': forms.TextInput(attrs={
                'class': 'form-control contact__section-input'
            }),

            'flat': forms.TextInput(attrs={
                'class': 'form-control contact__section-input'
            }),
        }
