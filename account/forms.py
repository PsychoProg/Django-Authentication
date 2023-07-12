from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from account.models import CustomUser
# validators
from django.core import validators


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = CustomUser
        fields = ["email"]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ["email", "password", "fullname", "phone"]


class LoginForm(forms.Form):
    """ login form class """
    # validate use validators
    # phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'fa fa-phone'}),
    #                         validators=[validators.MaxLengthValidator(11), start_with_zero])

    # phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'fa fa-phone'}),)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'fa fa-email'}),)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'fa fa-lock'}))
    # slug = forms.SlugField()
    # use validators
    # slug = forms.CharField(validators=[validators.validate_slug])

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            domain = email.split('@')[1]
            if domain != 'gmail.com':
                raise forms.ValidationError('only gmail.com email addresses are allowed.')

        return email

    # def clean_phone(self):
    #     phone = self.cleaned_data.get('phone')
    #     if len(phone) > 11 or len(phone) < 11:
    #         raise ValidationError('invalid phone number', code='phone_len_error')
    #
    #     if phone[0] != 0:
    #         raise ValidationError('phone number should start with 0!         ')
    #     return phone

    # def clean(self):
    #     """ use clean function for various type of errors """
    #     # cleaned data
    #     cd = super().clean()
    #     phone = cd['phone']
    #     if len(phone) > 11:
    #         raise ValidationError(
    #             'max phone len is 11 digits!!!',
    #             code='invalid',
    #             params={'value': f'{phone}'},
    #         )
    # add: for error in non_field_errors
