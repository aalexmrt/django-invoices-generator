from django.db import models
import datetime

class Company(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Client(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Invoice(models.Model):
    number = models.CharField(null=True, blank=True, max_length=100)
    date = models.DateField(null=True, blank=True)
    mailed = models.BooleanField(default=False)
    client = models.ForeignKey(Client, null=True, blank=True, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.number

    @classmethod
    def get_invoice_number(self):
        try:
            last_invoice = Invoice.objects.latest('id')
        except Invoice.DoesNotExist:
            last_invoice = None

        try:
            settings = Settings.objects.get(pk=1)
        except Invoice.DoesNotExist:
            settings = None

        if last_invoice is None:
            new_invoice_number = "{}-{:04d}".format(settings.year, 1)
        else:
            last_invoice = int(last_invoice.number.split("-")[1])
            new_invoice_number = "{}-{:04d}".format(settings.year, last_invoice + 1)

        return new_invoice_number

    def save(self, *args, **kwargs):
        if self.number is None:
            self.number = self.get_invoice_number()
        super(Invoice, self).save(*args, **kwargs)


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField(null=True, blank=True)
    invoice = models.ForeignKey(Invoice, blank=True, null=True, on_delete=models.CASCADE)
    def __str__(self):
            return self.name

class Settings(models.Model):
    year = models.IntegerField()
    prefix_invoicing = models.CharField(max_length=50)
    company = models.ForeignKey(Company, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return "Main settings"

    def save(self, *args, **kwargs):
        if not self.pk and Settings.objects.exists():
        # if you'll not check for self.pk
        # then error will also raised in update of exists model
            raise ValidationError('There is can be only one Settings instance')
        return super(Settings, self).save(*args, **kwargs)
