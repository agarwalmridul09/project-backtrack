from django import forms

from utilities.constants.RoleEnum import UserRole


class LoginForm(forms.Form):
    email = forms.EmailField(required=True, label='', widget=forms.EmailInput(attrs={
        "class": "form-control input-field",
        "placeholder": "Email Address"
    }))
    password = forms.CharField(required=True, label='', widget=forms.PasswordInput(attrs={
        "class": "form-control input-field",
        "placeholder": "Password"
    }))


class SignUpForm(forms.Form):
    first_name = forms.CharField(required=True, label='', widget=forms.TextInput(attrs={
        "class": "form-control input-field",
        "placeholder": "Last Name"
    }))
    last_name = forms.CharField(required=True, label='', widget=forms.TextInput(attrs={
        "class": "form-control input-field",
        "placeholder": "First Name"
    }))
    email = forms.EmailField(required=True, label='', widget=forms.EmailInput(attrs={
        "class": "form-control input-field",
        "placeholder": "Email Address"
    }))

    password = forms.CharField(required=True, label='', widget=forms.PasswordInput(attrs={
        "class": "form-control input-field",
        "placeholder": "Password"
    }))

    role = forms.CharField(required=True, label='', widget=forms.Select(choices=UserRole, attrs={
        "class": "form-control input-field",
        "placeholder": "Role",
    }))

    # email = models.EmailField(unique=True, null=False)
    # password = models.CharField(max_length=50, null=False)
    # USERNAME_FIELD = 'email'
    # first_name = models.CharField(max_length=50, null=False)
    # last_name = models.CharField(max_length=50, null=False)
    # role = models.CharField(max_length=2, choices=UserRole, default=DEVELOPER)
    # is_superuser = models.BooleanField(default=False)
    # is_staff = models.BooleanField(default=False)
    # is_active = models.BooleanField(default=False)
