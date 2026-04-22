from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import migrations, models
import django.db.models.deletion
import accounts.models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Profile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "avatar",
                    models.FileField(
                        blank=True,
                        upload_to=accounts.models.avatar_upload_path,
                        validators=[
                            FileExtensionValidator(
                                allowed_extensions=["jpg", "jpeg", "png", "gif", "webp"]
                            )
                        ],
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ServiceRequest",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=120, verbose_name="Название заявки")),
                ("customer_name", models.CharField(max_length=120, verbose_name="Имя клиента")),
                (
                    "device_type",
                    models.CharField(
                        choices=[
                            ("pc", "Стационарный ПК"),
                            ("laptop", "Ноутбук"),
                            ("monoblock", "Моноблок"),
                            ("other", "Другое устройство"),
                        ],
                        max_length=20,
                        verbose_name="Тип устройства",
                    ),
                ),
                ("problem_description", models.TextField(verbose_name="Описание проблемы")),
                ("estimated_price", models.DecimalField(decimal_places=2, max_digits=10, verbose_name="Оценочная стоимость")),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("new", "Новая"),
                            ("diagnostic", "Диагностика"),
                            ("repair", "В ремонте"),
                            ("done", "Завершена"),
                        ],
                        default="new",
                        max_length=20,
                        verbose_name="Статус",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")),
            ],
            options={
                "verbose_name": "Заявка на ремонт",
                "verbose_name_plural": "Заявки на ремонт",
                "ordering": ["-created_at"],
            },
        ),
    ]
