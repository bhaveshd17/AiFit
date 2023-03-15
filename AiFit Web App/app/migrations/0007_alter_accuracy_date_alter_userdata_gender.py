# Generated by Django 4.1.3 on 2023-03-15 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0006_alter_userdata_gender_accuracy"),
    ]

    operations = [
        migrations.AlterField(
            model_name="accuracy", name="date", field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name="userdata",
            name="gender",
            field=models.CharField(
                blank=True,
                choices=[(3, "Other"), (2, "Female"), (1, "Male")],
                max_length=20,
                null=True,
            ),
        ),
    ]
