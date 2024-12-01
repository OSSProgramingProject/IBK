# Generated by Django 5.1.3 on 2024-12-01 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IBK_ossproject', '0007_blogpost'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='visibility',
            field=models.CharField(choices=[('public', '전체공개'), ('private', '나만 보기')], default='public', max_length=10),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='category',
            field=models.CharField(max_length=100),
        ),
    ]
