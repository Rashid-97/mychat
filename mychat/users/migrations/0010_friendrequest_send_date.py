# Generated by Django 3.2.5 on 2021-12-07 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20211203_1015'),
    ]

    operations = [
        migrations.AddField(
            model_name='friendrequest',
            name='send_date',
            field=models.DateTimeField(auto_now_add=True, default='2021-09-02 13:05:40.780355'),
            preserve_default=False,
        ),
    ]
