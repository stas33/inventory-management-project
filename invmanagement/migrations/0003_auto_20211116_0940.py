# Generated by Django 3.2.8 on 2021-11-16 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invmanagement', '0002_auto_20211114_0958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='phone',
            field=models.IntegerField(null=True),
        ),
    ]
