# Generated by Django 3.1.7 on 2021-03-23 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='pick_up_comment',
            field=models.TextField(blank=True, null=True, verbose_name='Komentarz'),
        ),
    ]
