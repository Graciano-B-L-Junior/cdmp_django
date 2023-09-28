# Generated by Django 4.2.3 on 2023-09-28 14:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CDMP_APP', '0013_tetodegastosporcategoria'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Depositos',
            new_name='Receitas',
        ),
        migrations.AlterModelOptions(
            name='receitas',
            options={'verbose_name': 'Receita', 'verbose_name_plural': 'Receitas'},
        ),
        migrations.RenameField(
            model_name='receitas',
            old_name='data_deposito',
            new_name='data_receita',
        ),
    ]
