# Generated by Django 5.0.3 on 2025-07-02 03:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0004_rename_precio_unitario_pedido_precio_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='precio_total',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]
