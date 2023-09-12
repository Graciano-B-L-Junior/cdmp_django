# Generated by Django 4.2.3 on 2023-09-12 12:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CDMP_APP', '0008_alter_metafinanceira_icone'),
    ]

    operations = [
        migrations.CreateModel(
            name='TetoDeGastos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('janeiro', models.FloatField()),
                ('cliente', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='CDMP_APP.cliente')),
            ],
        ),
    ]
