from django.contrib.auth.models import User
from django import forms

class SiteUserLoginForm(forms.Form):
    username = forms.CharField(label='Username',
                               widget=forms.TextInput(attrs={
                                                'class': 'form-control',
                                                'name': 'username',
                                                'placeholder': 'Enter Username',
                                                'autofocus': "autofocus"
                                            })
                               )
    password = forms.CharField(label='Password',
                                widget=forms.PasswordInput(attrs={
                                    'class': 'form-control',
                                    'name': 'password',
                                    'placeholder': 'Enter Password'
                                }))
    class Meta:
        model = User
        # fields = ['username', 'password']
        #
        # widgets = {
        #     'username': TextInput(attrs={
        #         'class': 'form-control',
        #         'name': 'username',
        #         'placeholder': 'Enter Username'
        #     }),
        #     'password': PasswordInput(attrs={
        #         'class': 'form-control',
        #         'name': 'password',
        #         'placeholder': 'Enter Password'
        #     }),
        # }
