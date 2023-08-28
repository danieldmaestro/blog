# Generated by Django 4.2.3 on 2023-08-27 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0002_remove_post_category_post_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'room_table',
            },
        ),
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.ManyToManyField(blank=True, related_name='posts', to='blog_app.category'),
        ),
    ]