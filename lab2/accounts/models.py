from pathlib import Path

from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models


def avatar_upload_path(instance, filename):
    extension = Path(filename).suffix.lower() or ".jpg"
    return f"avatars/user_{instance.user_id}/profile{extension}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = models.FileField(
        upload_to=avatar_upload_path,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png", "gif", "webp"])],
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Profile for {self.user.username}"


class ServiceRequest(models.Model):
    DEVICE_CHOICES = [
        ("pc", "Стационарный ПК"),
        ("laptop", "Ноутбук"),
        ("monoblock", "Моноблок"),
        ("other", "Другое устройство"),
    ]

    STATUS_CHOICES = [
        ("new", "Новая"),
        ("diagnostic", "Диагностика"),
        ("repair", "В ремонте"),
        ("done", "Завершена"),
    ]

    title = models.CharField(max_length=120, verbose_name="Название заявки")
    customer_name = models.CharField(max_length=120, verbose_name="Имя клиента")
    device_type = models.CharField(max_length=20, choices=DEVICE_CHOICES, verbose_name="Тип устройства")
    problem_description = models.TextField(verbose_name="Описание проблемы")
    estimated_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Оценочная стоимость")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new", verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Заявка на ремонт"
        verbose_name_plural = "Заявки на ремонт"

    def __str__(self):
        return f"{self.title} ({self.customer_name})"
