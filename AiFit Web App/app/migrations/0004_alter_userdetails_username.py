# Generated by Django 4.1.3 on 2023-04-26 18:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("app", "0003_alter_userdetails_age"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userdetails",
            name="username",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_details",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
