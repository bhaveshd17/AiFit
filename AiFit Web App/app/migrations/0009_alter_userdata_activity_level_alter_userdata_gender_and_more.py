# Generated by Django 4.1.3 on 2023-03-10 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_alter_userdata_activity_level_alter_userdata_gender_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdata',
            name='activity_level',
            field=models.CharField(blank=True, choices=[(2, 'Lightly active'), (4, 'Very active'), (1, 'Sedentary'), (3, 'Moderatly active')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='gender',
            field=models.CharField(blank=True, choices=[(1, 'Male'), (2, 'Female'), (3, 'Other')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='main_goal',
            field=models.CharField(blank=True, choices=[(3, 'Keep Fit'), (1, 'Loose Weight'), (2, 'Build Muscels')], max_length=20, null=True),
        ),
    ]
