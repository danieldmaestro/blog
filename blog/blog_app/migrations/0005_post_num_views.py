# Generated by Django 4.1.7 on 2023-04-14 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0004_rename_create_date_post_publish_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='num_views',
            field=models.PositiveIntegerField(default=0),
        ),
    ]