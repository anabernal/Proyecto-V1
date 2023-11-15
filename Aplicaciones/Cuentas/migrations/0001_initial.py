# Generated by Django 4.2.6 on 2023-10-07 12:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ciudad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('departamento', models.CharField(max_length=30)),
                ('codigoPostal', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaIngreso', models.DateTimeField()),
                ('calificacion', models.CharField(max_length=100)),
                ('estado', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CuentaBancaria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nroCuenta', models.CharField(max_length=100, unique=True, verbose_name='Numero de Cuenta')),
                ('estado', models.CharField(max_length=100)),
                ('saldo', models.FloatField(verbose_name='Saldo')),
                ('nroContrato', models.CharField(max_length=100)),
                ('costoMantenimiento', models.DecimalField(decimal_places=2, max_digits=10)),
                ('promedioAcreditacion', models.DecimalField(decimal_places=2, max_digits=10)),
                ('tipoCuenta', models.CharField(choices=[('CC', 'Cuenta Corriente'), ('CA', 'Caja de Ahorro')], max_length=50, verbose_name='Tipo de Cuenta')),
                ('moneda', models.CharField(choices=[('PYG', 'GUARANIES'), ('USD', 'DOLARES'), ('EUR', 'EURO')], max_length=5, verbose_name='Moneda')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Cuentas.cliente')),
            ],
        ),
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('apellido', models.CharField(max_length=100)),
                ('tipoDocumento', models.CharField(max_length=100)),
                ('nroDocumento', models.CharField(max_length=100)),
                ('direccion', models.CharField(max_length=100)),
                ('celular', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('ciudad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Cuentas.ciudad')),
            ],
        ),
        migrations.CreateModel(
            name='Movimiento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaMovimiento', models.DateTimeField(auto_now_add=True)),
                ('tipoMovimiento', models.CharField(choices=[('DEP', 'DEPOSITO'), ('RET', 'RETIRO'), ('DEB', 'DEBITO'), ('CRE', 'CREDITO')], max_length=5, verbose_name='Tipo Movimiento')),
                ('saldoAnterior', models.DecimalField(decimal_places=2, max_digits=15)),
                ('saldoActual', models.DecimalField(decimal_places=2, max_digits=15)),
                ('montoMovimiento', models.FloatField()),
                ('cuentaOrigen', models.CharField(max_length=50, verbose_name='Cuenta Origen')),
                ('cuentaDestino', models.CharField(max_length=50, verbose_name='Cuenta Destino')),
                ('canal', models.CharField(choices=[('WEB', 'WEB'), ('CAJA', 'CAJA'), ('CAJERO', 'CAJERO'), ('APP', 'APP')], max_length=15)),
                ('cuenta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Cuentas.cuentabancaria')),
            ],
        ),
        migrations.AddField(
            model_name='cliente',
            name='persona',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Cuentas.persona'),
        ),
    ]
