# Generated by Django 4.2.3 on 2023-08-19 13:59

import core.custom_validators.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_appuser_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True, validators=[core.custom_validators.validators.validate_email]),
        ),
    ]
