# Generated by Django 4.0.2 on 2022-02-21 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Subscribers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(help_text='email adress', max_length=100)),
                ('full_name', models.CharField(help_text='first and last name ', max_length=100)),
            ],
        ),
    ]
