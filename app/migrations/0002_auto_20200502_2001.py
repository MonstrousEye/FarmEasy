# Generated by Django 3.0.5 on 2020-05-02 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='name',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='student',
            name='phone',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='student',
            name='roll',
            field=models.CharField(default='', max_length=50),
        ),
    ]
