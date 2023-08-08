# Generated by Django 4.2.3 on 2023-08-05 21:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CDMP_APP', '0004_historicomodificaoes'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricoCliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('operacao', models.CharField(max_length=100)),
                ('data_operacao', models.DateTimeField()),
            ],
            options={
                'verbose_name': 'HistoricoCliente',
                'verbose_name_plural': 'HistoricoClientes',
            },
        ),
        migrations.AlterModelOptions(
            name='categoria',
            options={'verbose_name': 'Categoria', 'verbose_name_plural': 'Categorias'},
        ),
        migrations.AlterModelOptions(
            name='cliente',
            options={'verbose_name': 'Cliente', 'verbose_name_plural': 'Clientes'},
        ),
        migrations.AlterModelOptions(
            name='depositos',
            options={'verbose_name': 'Deposito', 'verbose_name_plural': 'Depositos'},
        ),
        migrations.AlterModelOptions(
            name='gasto',
            options={'verbose_name': 'Gasto', 'verbose_name_plural': 'Gastos'},
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='depositos',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='gastos',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='metas',
        ),
        migrations.AddField(
            model_name='depositos',
            name='cliente',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='CDMP_APP.cliente'),
        ),
        migrations.AddField(
            model_name='gasto',
            name='cliente',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='CDMP_APP.cliente'),
        ),
        migrations.AddField(
            model_name='metafinanceira',
            name='cliente',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='CDMP_APP.cliente'),
        ),
        migrations.AlterField(
            model_name='gasto',
            name='categoria',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='CDMP_APP.categoria'),
        ),
        migrations.DeleteModel(
            name='HistoricoModificaoes',
        ),
        migrations.AddField(
            model_name='historicocliente',
            name='cliente',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='CDMP_APP.cliente'),
        ),
    ]
