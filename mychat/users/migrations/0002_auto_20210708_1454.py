# Generated by Django 3.2.5 on 2021-07-08 10:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='siteuser',
            name='join_date',
        ),
        migrations.RemoveField(
            model_name='siteuser',
            name='name',
        ),
        migrations.RemoveField(
            model_name='siteuser',
            name='password',
        ),
        migrations.RemoveField(
            model_name='siteuser',
            name='status',
        ),
        migrations.RemoveField(
            model_name='siteuser',
            name='username',
        ),
    ]
