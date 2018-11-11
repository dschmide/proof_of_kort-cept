# Generated by Django 2.0.5 on 2018-11-11 18:07

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('restful_api', '0006_auto_20181109_1703'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlacedTower',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', django.contrib.postgres.fields.ArrayField(base_field=models.DecimalField(decimal_places=15, max_digits=17), size=None)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('creator',),
            },
        ),
    ]
