# Generated by Django 4.2.3 on 2023-09-28 14:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CDMP_APP', '0014_rename_depositos_receitas_alter_receitas_options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tetodegastosporcategoria',
            old_name='abril',
            new_name='teto',
        ),
        migrations.RemoveField(
            model_name='tetodegastosporcategoria',
            name='agosto',
        ),
        migrations.RemoveField(
            model_name='tetodegastosporcategoria',
            name='dezembro',
        ),
        migrations.RemoveField(
            model_name='tetodegastosporcategoria',
            name='fevereiro',
        ),
        migrations.RemoveField(
            model_name='tetodegastosporcategoria',
            name='janeiro',
        ),
        migrations.RemoveField(
            model_name='tetodegastosporcategoria',
            name='julho',
        ),
        migrations.RemoveField(
            model_name='tetodegastosporcategoria',
            name='junho',
        ),
        migrations.RemoveField(
            model_name='tetodegastosporcategoria',
            name='maio',
        ),
        migrations.RemoveField(
            model_name='tetodegastosporcategoria',
            name='marco',
        ),
        migrations.RemoveField(
            model_name='tetodegastosporcategoria',
            name='novembro',
        ),
        migrations.RemoveField(
            model_name='tetodegastosporcategoria',
            name='outubro',
        ),
        migrations.RemoveField(
            model_name='tetodegastosporcategoria',
            name='setembro',
        ),
    ]
