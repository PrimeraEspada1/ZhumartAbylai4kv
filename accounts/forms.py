from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


image_validator = FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png", "gif", "webp"])


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")
    avatar = forms.FileField(
        required=False,
        label="Фото профиля",
        validators=[image_validator],
        help_text="Поддерживаются JPG, JPEG, PNG, GIF и WEBP.",
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "avatar")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            avatar = self.cleaned_data.get("avatar")
            if avatar:
                user.profile.avatar = avatar
                user.profile.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Логин")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)


class ProfileAvatarForm(forms.Form):
    avatar = forms.FileField(
        required=True,
        label="Новое фото профиля",
        validators=[image_validator],
        help_text="Загрузите только изображение.",
    )
