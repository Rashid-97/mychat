# Generated by Django 3.2.5 on 2021-12-03 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_friendrequest_accepted_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='friendrequest',
            old_name='accepted_date',
            new_name='reaction_date',
        ),
        migrations.AddField(
            model_name='friendrequest',
            name='status',
            field=models.BooleanField(null=True),
        ),
    ]
