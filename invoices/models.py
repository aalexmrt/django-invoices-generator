import logging
from django.db import models


class Address(models.Model):
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(null=True, blank=True, max_length=100)
    postal_code = models.CharField(max_length=100)
    country = models.CharField(null=True, blank=True, max_length=100)
    alias = models.CharField(null=True, blank=True,
                             max_length=100, default='Default')

    def __str__(self):
        return f'{self.street}, {self.postal_code}, {self.city}'

    class Meta:
        ordering = ['alias']


class Contact(models.Model):
    name = models.CharField(null=True, blank=True, max_length=100)
    phone_number = models.CharField(null=True, blank=True, max_length=100)
    email = models.CharField(null=True, blank=True, max_length=100)
    cc_email = models.CharField(null=True, blank=True, max_length=100)
    country = models.CharField(null=True, blank=True, max_length=100)

    def __str__(self):
        return self.name


class Company(models.Model):
    address = models.ForeignKey(
        Address, on_delete=models.CASCADE, null=True, blank=True)
    contact = models.ForeignKey(
        Contact, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    bank_account_number = models.CharField(
        null=True, blank=True, max_length=100)
    customer_information_file_number = models.CharField(max_length=100)
    logo = models.ImageField(null=True, blank=True, upload_to='company/images')

    def __str__(self):
        if self.name is None:
            return self.id
        return self.name

    class Meta:
        ordering = ['name']


class Issuer(models.Model):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        if self.company is None:
            return str(self.id)
        return str(self.company)


class Customer(models.Model):
    company = models.ForeignKey(
        Company, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        if self.company is None:
            return str(self.id)
        return str(self.company)


class MailInfo(models.Model):
    STATUS_CHOICES = (
        ("Pending", "Pending"),
        ("Failed", "Failed"),
        ("Delivered", "Delivered")
    )
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="Pending")
    sent_timestamp = models.DateTimeField(default=None, null=True, blank=True)

    def __str__(self):
        return self.status


class GlobalSettings(models.Model):
    issuer = models.ForeignKey(
        Issuer, null=True, blank=True, on_delete=models.CASCADE)

    discount_value = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True, default=0)
    last_number = models.IntegerField(null=True, blank=True, default=0)
    lead_zeros_format = models.IntegerField(null=True, blank=True, default=0)
    sequence = models.CharField(null=True, blank=True, max_length=100)
    tax_value = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True, default=0)

    def __str__(self):
        return "Global settings"

    @property
    def default_issuer(self):
        return self.issuer

    @property
    def default_discount_value(self):
        return self.discount_value

    @property
    def default_lead_zeros_format(self):
        return self.lead_zeros_format

    @property
    def default_sequence(self):
        return self.sequence

    @property
    def default_tax_value(self):
        return self.tax_value

    def increase_last_number(self):
        if self.last_number is None:
            self.last_number = 0
        self.last_number += 1
        self.save()
        return self.last_number


class Invoice(models.Model):
    issuer = models.ForeignKey(
        Issuer, null=True, blank=True, on_delete=models.CASCADE)
    customer = models.ForeignKey(
        Customer, null=True, blank=True, on_delete=models.CASCADE)
    global_settings = models.ForeignKey(
        GlobalSettings, null=True, blank=True, on_delete=models.CASCADE)
    mail_info = models.OneToOneField(
        MailInfo, null=True, blank=True, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    discount_amount = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True, default=0)
    discount_value = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True, default=0)
    issued_date = models.DateField(null=True, blank=True)
    number = models.IntegerField(null=True, blank=True)
    pdf_document = models.FileField(upload_to='invoices_pdf/')
    sequence = models.CharField(null=True, blank=True, max_length=100)
    sub_total = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True, default=0)
    tax_amount = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True, default=0)
    tax_base = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True, default=0)
    tax_value = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True, default=0)
    total_due = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True, default=0)
    unique_code_number = models.CharField(
        null=True, blank=True, max_length=100, unique=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.global_settings = GlobalSettings.objects.filter().first()

        logging.info(f'Loaded global settings {self.global_settings}')

    def save(self, *args, **kwargs):
        if not self.issuer:
            self.issuer = self.global_settings.default_issuer
        if not self.sequence:
            self.sequence = self.global_settings.default_sequence
        if not self.number:
            self.number = self.global_settings.increase_last_number()
        if not self.discount_value and not self.tax_value:
            self.discount_value = self.global_settings.default_discount_value
            self.tax_value = self.global_settings.default_tax_value

        super().save(*args, **kwargs)

    @property
    def sequence_number(self):
        if self.sequence and self.number:
            formatted_number = str(self.number).zfill(
                self.global_settings.default_lead_zeros_format)
            return f"{self.sequence}-{formatted_number}"
        else:
            return f"Database id: {self.id}"

    def calculate_totals(self, orders):
        self.sub_total = self.discount_amount = self.tax_base = self.tax_amount = self.total_due = 0
        for current_order in orders:
            self.sub_total += current_order.line_total

        self.discount_amount = self.sub_total * self.discount_value / 100
        self.tax_base = self.sub_total - self.discount_amount
        self.tax_amount = self.tax_base * self.tax_value / 100
        self.total_due = self.tax_base + self.tax_amount

    def __str__(self):
        return self.sequence_number


class Product(models.Model):
    name = models.CharField(null=True, blank=True, max_length=100)
    price = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name

    def default_unit_price(self):
        return self.price
    
    class Meta:
        ordering = ['name']


class OrderLine(models.Model):
    product = models.ForeignKey(
        to=Product, on_delete=models.CASCADE)
    invoice = models.ForeignKey(to=Invoice, on_delete=models.CASCADE)
    quantity = models.DecimalField(
        max_digits=6, decimal_places=3, null=True, blank=True, default=0)
    unit_price = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True, default=0)
    line_total = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)

    # def __str__(self):
    #     return f"Related invoice: {self.invoice.get_sequence_number()}"

    def save(self, *args, **kwargs):
        # set default unit price if not already set
        if not self.unit_price:
            self.unit_price = self.product.default_unit_price()

        # get line total
        self.line_total = self.quantity * self.unit_price

        super(OrderLine, self).save(*args, **kwargs)
