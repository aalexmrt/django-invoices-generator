from django.db import models


class Address(models.Model):
    street = models.CharField(null=True, blank=True, max_length=100)
    city = models.CharField(null=True, blank=True, max_length=100)
    state = models.CharField(null=True, blank=True, max_length=100)
    postal_code = models.CharField(null=True, blank=True, max_length=100)
    country = models.CharField(null=True, blank=True, max_length=100)

    def __str__(self):
        return self.street


class Contact(models.Model):
    name = models.CharField(null=True, blank=True, max_length=100)
    phone_number = models.CharField(null=True, blank=True, max_length=100)
    email = models.CharField(null=True, blank=True, max_length=100)
    # TODO: convert cc_email to a list of emails, it can be 0, 1 or more emails in this field
    cc_email = models.CharField(null=True, blank=True, max_length=100)
    country = models.CharField(null=True, blank=True, max_length=100)

    def __str__(self):
        return self.name


class Company(models.Model):
    address = models.ForeignKey(
        Address, on_delete=models.CASCADE, null=True, blank=True)
    contact = models.ForeignKey(
        Contact, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(null=True, blank=True, max_length=100)
    bank_account_number = models.CharField(
        null=True, blank=True, max_length=100)
    customer_information_file_number = models.CharField(
        null=True, blank=True, max_length=100)

    def __str__(self):
        return self.name


class Issuer(models.Model):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.company.name


class Customer(models.Model):
    company = models.ForeignKey(
        Company, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.company.name


class Product(models.Model):
    name = models.CharField(null=True, blank=True, max_length=100)
    price = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name


class MailInfo(models.Model):
    STATUS_CHOICES = (
        ("Pending", "Pending"),
        ("Failed", "Failed"),
        ("Delivered", "Delivered")
    )
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="Pending")
    sent_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.status


class Invoice(models.Model):

    issuer = models.ForeignKey(
        Issuer, null=True, blank=True, on_delete=models.CASCADE)
    customer = models.ForeignKey(
        Customer, null=True, blank=True, on_delete=models.CASCADE)
    mail_info = models.OneToOneField(
        MailInfo, null=True, blank=True, on_delete=models.CASCADE)
    pdf_document = models.FileField(upload_to='invoices_pdf/')
    sequence = models.CharField(null=True, blank=True, max_length=100)
    number = models.IntegerField(null=True, blank=True)
    discount_value = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True, default=0)
    discount_amount = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True, default=0)
    tax_value = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True, default=0)
    tax_amount = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True, default=0)
    sub_total = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True, default=0)
    total_due = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True, default=0)
    issued_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_sequence_number(self):
        if self.sequence and self.number:
            return f"{self.sequence}-{self.number}"
        else:
            return f"Database id: {self.id}"

    def do_operations(self, orders):
        self.discount_amount = self.sub_total = self.tax_amount = self.total_due = 0

        for current_order in orders:
            # self.discount_amount += current_order.discount_amount
            self.sub_total += current_order.line_total
            # self.tax_amount += current_order.tax_amount
            # self.total_due += current_order.line_total

        print("hello")
        print(orders)

    def __str__(self):
        return self.get_sequence_number()


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

    def __str__(self):
        return "test"

    def save(self, *args, **kwargs):
        # get line total
        self.line_total = self.quantity * self.unit_price

        super(OrderLine, self).save(*args, **kwargs)

    def __str__(self):
        object = str(self.id)
        return object
