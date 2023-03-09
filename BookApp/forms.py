from django import forms
from .models import Book, Stage, Language, Category
from django.contrib.auth.models import User

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = "__all__"

        widgets = {
            'title': forms.TextInput(
                attrs={
                    'placeholder': 'title',
                    'class': 'single',
                }
            ),
            'author': forms.TextInput(
                attrs={
                    'placeholder': 'author',
                    'class': 'single',
                }
            ),
            'isbn': forms.TextInput(
                attrs={
                    'placeholder': 'isbn',
                    'class': 'single',
                }
            ),
            'publishedDate': forms.TextInput(
                attrs={
                    'placeholder': 'publishedDate',
                    'class': 'single',
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'placeholder': 'description',
                    'class': 'multi',
                }
            ),
            'impression': forms.Textarea(
                attrs={
                    'placeholder': 'impression',
                    'class': 'multi',
                }
            ),
            'page': forms.NumberInput(
                attrs={
                    'min': '0',
                }
            ),
            'review': forms.NumberInput(
                attrs={
                    'min': '1',
                    'max': '5',
                }
            ),

        }    


class StageForm(forms.ModelForm):
    class Meta:
        model = Stage
        fields = "__all__"

        widgets = {
            'title': forms.TextInput(
                attrs={
                    'placeholder': 'stage',
                    'class': 'single',
                }
            ),
        }


class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = "__all__"

        widgets = {
            'title': forms.TextInput(
                attrs={
                    'placeholder': 'stage',
                    'class': 'single',
                }
            ),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"

        widgets = {
            'title': forms.TextInput(
                attrs={
                    'placeholder': 'stage',
                    'class': 'single',
                }
            ),
        }


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('last_name', 'first_name', 'username', 'email')

        widgets = {
            'last_name': forms.TextInput(
                attrs={
                    'placeholder': 'last_name',
                    'class': 'single',
                }
            ),
            'first_name': forms.TextInput(
                attrs={
                    'placeholder': 'first_name',
                    'class': 'single',
                }
            ),
            'username': forms.TextInput(
                attrs={
                    'placeholder': 'username',
                    'class': 'single',
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'placeholder': 'email',
                    'class': 'single',
                }
            ),
        }


class AccountForm(forms.Form):
    username = forms.CharField(
        max_length = 30,
        widget = forms.TextInput(
            attrs = {
                'placeholder':'Username',
                'class':'single'
            }
        )
    )

    password = forms.CharField(
        max_length = 128,
        widget = forms.PasswordInput(
            attrs={
                'placeholder':'Password', 
                'class':'single'
            }
        )
    )