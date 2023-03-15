# Generated by Django 4.1.3 on 2023-03-08 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_record_video_alter_userdata_gender'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdata',
            name='target_weight',
        ),
        migrations.AddField(
            model_name='userdata',
            name='main_goal',
            field=models.CharField(blank=True, choices=[(2, 'Build Muscels'), (1, 'Loose Weight'), (3, 'Keep Fit')], max_length=20, null=True),
        ),
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
    ]