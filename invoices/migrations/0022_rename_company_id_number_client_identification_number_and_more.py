# Generated by Django 4.1.5 on 2023-02-26 09:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0021_contact_remove_client_email_remove_company_email'),
    ]

    operations = [
        migrations.RenameField(
            model_name='client',
            old_name='company_id_number',
            new_name='identification_number',
        ),
        migrations.RenameField(
            model_name='company',
            old_name='company_id_number',
            new_name='identification_number',
        ),
        migrations.AddField(
            model_name='client',
            name='additional_contact',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='additional_contacts', to='invoices.contact'),
        ),
        migrations.AddField(
            model_name='client',
            name='primary_contact',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='primary_contact', to='invoices.contact'),
        ),
    ]
