# Generated by Django 3.2.5 on 2021-07-28 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_friendlist_has_blocked'),
    ]

    operations = [
        migrations.RenameField(
            model_name='friendlist',
            old_name='has_blocked',
            new_name='had_been_blocked',
        ),
        migrations.AddField(
            model_name='friendlist',
            name='had_blocked',
            field=models.BooleanField(default=False),
        ),
    ]