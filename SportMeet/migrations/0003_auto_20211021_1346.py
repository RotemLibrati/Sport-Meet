# Generated by Django 3.2.8 on 2021-10-21 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SportMeet', '0002_team_teamprivileges'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='address',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='profile',
            name='age',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='profile',
            name='sex',
            field=models.CharField(choices=[('male', 'male'), ('female', 'female')], default='male', max_length=10),
            preserve_default=False,
        ),
    ]