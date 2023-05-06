# Generated by Django 4.2 on 2023-05-03 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TestResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_id', models.CharField(max_length=255, null=True)),
                ('age', models.IntegerField(null=True)),
                ('gender', models.CharField(max_length=10, null=True)),
                ('speciality', models.CharField(max_length=30, null=True)),
                ('city', models.CharField(max_length=30, null=True)),
                ('test1', models.IntegerField(blank=True, null=True)),
                ('test2', models.IntegerField(blank=True, null=True)),
                ('test3', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]