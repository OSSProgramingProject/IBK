# Generated by Django 5.1.3 on 2024-12-01 17:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('IBK_ossproject', '0009_blogpost_contest_id_blogpost_index_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpost',
            name='updated_at',
        ),
    ]
