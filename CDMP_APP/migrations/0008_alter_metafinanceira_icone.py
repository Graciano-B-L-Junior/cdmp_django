# Generated by Django 4.2.3 on 2023-08-27 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CDMP_APP', '0007_rename_gasto_despesa_alter_despesa_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metafinanceira',
            name='icone',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
