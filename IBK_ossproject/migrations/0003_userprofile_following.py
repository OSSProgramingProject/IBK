# Generated by Django 5.1.3 on 2024-11-28 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IBK_ossproject', '0002_remove_userprofile_user_name_userprofile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='following',
            field=models.ManyToManyField(blank=True, related_name='followers', to='IBK_ossproject.userprofile'),
        ),
    ]
