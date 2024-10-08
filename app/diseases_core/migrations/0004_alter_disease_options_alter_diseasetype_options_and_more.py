# Generated by Django 5.1.1 on 2024-09-29 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diseases_core', '0003_rename_specific_for_gender_disease_specific_gender'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='disease',
            options={'ordering': ['-pk'], 'verbose_name': 'Disease', 'verbose_name_plural': 'Diseases'},
        ),
        migrations.AlterModelOptions(
            name='diseasetype',
            options={'ordering': ['-pk'], 'verbose_name': 'Disease Type', 'verbose_name_plural': 'Disease Types'},
        ),
        migrations.AddField(
            model_name='disease',
            name='umls_id',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
