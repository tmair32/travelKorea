from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from django.contrib.auth import get_user_model
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
from django.contrib import auth
from django import forms
from django.forms import ModelForm
from .models import MyUser

class SignupForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['email', 'password1', 'password2', 'username','gender', 'birth',]
    
    # def clean(self):
    #     form_data = self.cleaned_data
    #     if form_data.get('password1'):
    #         if form_data['password1'] != form_data['password2']:
    #             self._errors["password1"] = [""] # Will raise a error message
    #             self._errors["password2"] = ["비밀번호가 일치하지 않습니다"]
    #             del form_data['password1']

    #     if form_data.get('email'):
    #         if get_user_model().objects.filter(email=form_data['email']).exists():
    #             self._errors['email'] = ['이메일이 중복되었습니다']

    #     return form_data
        # GENDER_CHOICE = (
        #     ('남', '남'), ('여', '여')
        # )
        # widgets = {
        #     'gender': forms.Select(choices=GENDER_CHOICE),
        # }

class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        class_update_fields = ['username', 'password']
        for field_name in class_update_fields:
            self.fields[field_name].widget.attrs.update({
                'class': 'form-control'
            })
