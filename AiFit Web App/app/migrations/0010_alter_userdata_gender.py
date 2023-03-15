# Generated by Django 4.1.3 on 2023-03-15 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0009_alter_accuracy_date_alter_userdata_gender"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userdata",
            name="gender",
            field=models.CharField(
                blank=True,
                choices=[(2, "Female"), (3, "Other"), (1, "Male")],
                max_length=20,
                null=True,
            ),
        ),
    ]
