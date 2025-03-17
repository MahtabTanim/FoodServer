from account.models import User
from django import forms


def getUserPass(request):
    return request.user.password


class PassWordChangeForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = [
            "password",
            "confirm_password",
        ]

    def clean(self):
        cleaned_data = super(PassWordChangeForm, self).clean()
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
