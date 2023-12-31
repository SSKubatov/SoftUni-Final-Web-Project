# Generated by Django 3.2.7 on 2023-06-27 14:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_urlproperty'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_property', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='courses.fileproperty')),
                ('url_property', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='courses.urlproperty')),
                ('video', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='resources', to='courses.video')),
            ],
        ),
    ]
