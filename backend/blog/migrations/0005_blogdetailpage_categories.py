# Generated by Django 4.0.2 on 2022-03-03 08:44

from django.db import migrations
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_blogcategory_alter_blogauthorsorderable_page'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogdetailpage',
            name='categories',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, to='blog.BlogCategory'),
        ),
    ]
