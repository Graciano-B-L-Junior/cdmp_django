# Generated by Django 4.2.3 on 2023-09-28 13:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CDMP_APP', '0011_categoria_cliente'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicocliente',
            name='meta_financeira',
        ),
        migrations.DeleteModel(
            name='MetaFinanceira',
        ),
    ]
