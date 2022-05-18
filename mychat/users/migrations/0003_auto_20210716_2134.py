# Generated by Django 3.2.5 on 2021-07-16 17:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0002_auto_20210708_1454'),
    ]

    operations = [
        migrations.AddField(
            model_name='friendlist',
            name='room_id',
            field=models.CharField(default='None', max_length=50),
        ),
        migrations.AlterField(
            model_name='siteuser',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='siteuser', to=settings.AUTH_USER_MODEL),
        ),
    ]
