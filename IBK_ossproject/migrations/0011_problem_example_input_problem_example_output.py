# Generated by Django 5.1.3 on 2024-12-02 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IBK_ossproject', '0010_remove_problem_options_remove_problem_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='example_input',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='problem',
            name='example_output',
            field=models.TextField(blank=True, null=True),
        ),
    ]
