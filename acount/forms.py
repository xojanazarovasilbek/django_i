from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError


class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(label='Parol', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Parolni tasdiqlang', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {
            'username': 'Login',
            'first_name': 'Ism',
            'last_name': 'Familiya',
            'email': 'Email',
            
        }
        help_texts = {
            'username': '',  
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("Bu foydalanuvchi nomi allaqachon mavjud.")
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if not password1 or not password2 or password1 != password2:
            raise forms.ValidationError('Parollar mos emas.')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=120, label='Login')
    password = forms.CharField(label='Parol', widget=forms.PasswordInput)

class ChangePassForm(forms.Form):
    ol_pass = forms.CharField(label='eski parol', widget=forms.PasswordInput)
    new_pass = forms.CharField(label='yangi parol', widget=forms.PasswordInput)
    confrim_pass = forms.CharField(label='parolni tastiqlang', widget=forms.PasswordInput)
    code = forms.CharField(label='Email yuborilgan kod', max_length=6)





    # def clean(self):
    #     cleaned_data = super().clean()
    #     new_pass = cleaned_data.get("new_pass")
    #     confirm_pass = cleaned_data.get("confirm_pass")

    #     if new_pass != confirm_pass:
    #         raise forms.ValidationError("tasdiqlash paroli mos emas!")


    def clean(self):
        cleaned_data = super().clean()
        new_pass = cleaned_data.get("new_pass")
        confirm_pass = cleaned_data.get("confirm_pass")

        if new_pass and confirm_pass and new_pass != confirm_pass:
            self.add_error('confirm_pass', "Yangi parol va tasdiqlash paroli bir xil emas.")




class ResetPassForm(forms.Form):
    password = forms.CharField(label='Yangi parol',widget=forms.PasswordInput)
    password_confirm = forms.CharField(label='Yangi parolni tasdiqlang',widget=forms.PasswordInput)
    code = forms.CharField(label='Tastiqlash kodi',max_length=6)


    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            raise forms.ValidationError("Yangi parol va tasdiqlash paroli mos emas!")

