from django import forms
from .models import User, UserProfile
from vendor.models import Vendor
from .validators import allow_only_image_validator


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "phone_number",
            "password",
            "confirm_password",
        ]

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "Password Does not Match",
            )
        if len(password) < 8:
            raise forms.ValidationError(
                "Password Must have 8 or more characters",
            )


class VendorForm(forms.ModelForm):
    vendor_name = forms.CharField(
        max_length=100,
        help_text="Hello World",
        widget=forms.TextInput(attrs={"placeholder": "Enter Vendor Name"}),
    )
    vendor_licesnse = forms.ImageField(
        widget=forms.FileInput(attrs={"class": "btn btn-info"}),
        validators=[allow_only_image_validator],
    )

    class Meta:
        model = Vendor
        fields = [
            "vendor_name",
            "vendor_licesnse",
        ]


class UserProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field == "latitude" or field == "longitude":
                self.fields[field].widget.attrs["readonly"] = "readonly"

    profile_picture = forms.ImageField(
        widget=forms.FileInput(attrs={"class": "btn btn-info"}),
        validators=[allow_only_image_validator],
    )
    cover_photo = forms.ImageField(
        widget=forms.FileInput(attrs={"class": "btn btn-info"}),
        validators=[allow_only_image_validator],
    )
    address = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Start Typing......",
                "required": "required",
            }
        )
    )

    class Meta:
        model = UserProfile
        fields = [
            "profile_picture",
            "cover_photo",
            "address",
            "country",
            "state",
            "city",
            "pin_code",
            "latitude",
            "longitude",
        ]


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "phone_number",
        ]
