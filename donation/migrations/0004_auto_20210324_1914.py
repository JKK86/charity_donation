# Generated by Django 3.1.7 on 2021-03-24 19:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0003_auto_20210323_1742'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='categories',
            field=models.ManyToManyField(related_name='donations', to='donation.Category', verbose_name='Kategorie'),
        ),
        migrations.AlterField(
            model_name='donation',
            name='institution',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='donations', to='donation.institution', verbose_name='Instytucja'),
        ),
        migrations.AlterField(
            model_name='institution',
            name='categories',
            field=models.ManyToManyField(related_name='institutions', to='donation.Category', verbose_name='Kategorie'),
        ),
    ]