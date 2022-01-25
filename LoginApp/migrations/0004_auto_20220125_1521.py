# Generated by Django 2.2.25 on 2022-01-25 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LoginApp', '0003_usermodel_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='role',
            field=models.CharField(blank=True, choices=[('emp', 'emp'), ('admin', 'admin'), ('hr', 'hr')], default='emp', max_length=255, verbose_name='Role'),
        ),
    ]
