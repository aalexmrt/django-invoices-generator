# Generated by Django 4.1.5 on 2023-06-15 03:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0012_alter_invoice_unique_code_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='company/images'),
        ),
    ]
