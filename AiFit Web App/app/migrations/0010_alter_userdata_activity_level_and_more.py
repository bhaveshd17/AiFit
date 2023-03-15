# Generated by Django 4.1.3 on 2023-03-10 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_alter_userdata_activity_level_alter_userdata_gender_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdata',
            name='activity_level',
            field=models.CharField(blank=True, choices=[(1, 'Sedentary'), (2, 'Lightly active'), (3, 'Moderatly active'), (4, 'Very active')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='main_goal',
            field=models.CharField(blank=True, choices=[(1, 'Loose Weight'), (2, 'Build Muscels'), (3, 'Keep Fit')], max_length=20, null=True),
        ),
    ]