from django import forms
from django.contrib.auth.models import Permission , Group
from django.contrib.auth.forms import AuthenticationForm , PasswordChangeForm , PasswordResetForm  , SetPasswordForm
from django.contrib.auth.views import PasswordResetDoneView
from django.contrib.auth import authenticate
from users.models import CustomUser
from django.contrib.auth import get_user_model
User = get_user_model()

class StyledFormMixinextra:
    """ Mixing to apply style to form field"""

    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.apply_styled_widgets()

    default_classes = "w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-pink-500"

    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class': f"{self.default_classes}",
                    'placeholder': f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget, forms.PasswordInput):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget, forms.EmailField):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': f"{self.default_classes} resize-none",
                    'placeholder':  f"Enter {field.label.lower()}",
                    'rows': 5
                })
            elif isinstance(field.widget, forms.SelectDateWidget):
                field.widget.attrs.update({
                    "class": "border-2 border-gray-300 p-3 rounded-lg shadow-sm focus:outline-none focus:border-rose-500 focus:ring-rose-500"
                })
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class': "space-y-2"
                })
            else:
                field.widget.attrs.update({
                    'class': self.default_classes
                })
class EditUserProfileForm(StyledFormMixinextra, forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username','first_name','last_name','email','phone_number','bio','profile_photo']

class UserRegisterForm(StyledFormMixinextra , forms.ModelForm):
    password  = forms.CharField(widget=forms.PasswordInput , label="password")
    confirm_password = forms.CharField(widget=forms.PasswordInput , label="Confirm password" )
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password','confirm_password']
    
        widgets ={
            'email':forms.EmailInput(attrs={'placeholder':"Enter Your Email:"})
        }
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email = email).exists():
            raise forms.ValidationError("This Email Alrady Exit.")
        return email
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        errors = []
        if len(password)<=8:
            errors.append("Please give me atlist eight char Password.")
        if errors:
            raise forms.ValidationError(errors)
        return password
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        errors = []
        if password != confirm_password:
            errors.append("Password and confirm password are not same.")

        if errors:
            raise forms.ValidationError(errors)
        return cleaned_data

# login form:
class UserLoginForm(StyledFormMixinextra , AuthenticationForm):
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        errors = []
        if username and password:
            user = authenticate(username=username, password=password)
        if user is None:
            errors.append("Invalid username or password.")
        self.user = user

        if errors:
            raise forms.ValidationError(errors)
        return cleaned_data

class ChangeRoleForm(StyledFormMixinextra , forms.Form):
    choice_role = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        to_field_name='name',
        empty_label="Select a role"
    )

#form for create group
class GroupForm(StyledFormMixinextra ,forms.Form):
    name = forms.CharField(
        label="Group Name",
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter group name'
        })
    )
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Select Permissions"
    )

class CustomPasswordChangeForm(StyledFormMixinextra ,PasswordChangeForm):
    pass

class CustomPasswordResetForm(StyledFormMixinextra ,PasswordResetForm):
    pass

class CustomPasswordConfirmForm(StyledFormMixinextra , SetPasswordForm):
    pass