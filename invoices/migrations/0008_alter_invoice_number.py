# Generated by Django 4.1.5 on 2023-05-15 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0007_globalsettings_last_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='number',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
