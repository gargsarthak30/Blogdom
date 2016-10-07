from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class PasswordResetRequestForm(forms.Form):
    email_or_username = forms.CharField(label=("Email or Username"), max_length=254, widget=forms.TextInput(attrs={'class':'form-control'}))


class SetPasswordForm(forms.Form):
    error_messages = {
        'password_mismatch': "The two password fields didn't match!"
    }
    new_password1 = forms.CharField(label="New Passsword", widget=forms.PasswordInput)
    new_password2 = forms.CharField(label="New Password Confirmation", widget=forms.PasswordInput)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(self.error_messages['password_mismatch'], code='password_mismatch',)
        return password2


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email')

    def save(self, commit = True):
        User = super(RegistrationForm, self).save(commit=False)
        User.email = self.cleaned_data["email"]
        if commit:
            User.save()

        return User



