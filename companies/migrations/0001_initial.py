# Generated by Django 3.2.8 on 2021-11-08 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True, null=True)),
                ('address', models.CharField(max_length=100, null=True)),
                ('postcode', models.IntegerField(blank=True, default='0', null=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
    ]
