# Generated by Django 5.1.5 on 2025-03-17 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_alter_order_payment_method'),
        ('vendor', '0007_alter_openinghour_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total_data',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='vendors',
            field=models.ManyToManyField(blank=True, to='vendor.vendor'),
        ),
    ]
