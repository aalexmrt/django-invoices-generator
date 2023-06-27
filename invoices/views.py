import environ
from datetime import datetime
from django.core.files.base import ContentFile
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django_weasyprint.views import WeasyTemplateResponse
from invoices.forms import InvoiceForm, OrderLineFormSet
from invoices.models import (
    Customer,
    Invoice,
    Issuer,
    GlobalSettings,
    MailInfo,
    OrderLine,
    Product,
)
from invoices.utils.send_email import send_invoice_email

env = environ.Env()
env.read_env()


def index(request):

    if request.method == 'POST':
        data = request.POST
        ids_invoices = data.getlist('selected_options')

        send_invoices(ids_invoices)

        return HttpResponseRedirect(reverse('index'))

    invoices_list = Invoice.objects.order_by('-number')
    context = {
        'invoices_list': invoices_list
    }

    return render(request, 'invoices/index.html', context)


def add_invoice(request):

    new_invoice = Invoice.objects.create()
    new_invoice.save()
    return redirect('make_invoice', new_invoice.id)


def make_invoice(request, id):

    invoice = Invoice.objects.get(pk=id)
    order_lines = OrderLine.objects.filter(invoice=invoice)

    if request.method == 'POST':
        invoice_form = InvoiceForm(request.POST, instance=invoice)
        order_formset = OrderLineFormSet(
            request.POST, instance=invoice, queryset=order_lines)

        if invoice_form.is_valid():
            invoice = invoice_form.save()
            invoice.issuer = Issuer.objects.filter(
                company__name='issuer').first()
            invoice.mail_info = MailInfo.objects.create()
            invoice.save()

        if order_formset.is_valid():
            invoice_orders = []
            for order_form in order_formset:
                order = order_form.save(commit=False)
                order.invoice = invoice
                try:
                    product = Product.objects.get(
                        pk=order_form.cleaned_data["product"].id)
                    order.product = product
                    order.save()
                    invoice_orders.append(order)
                except:
                    pass

            order_formset.save()
            invoice.calculate_totals(invoice_orders)
            invoice.save()
            save_invoice_pdf(request, id)

            return redirect('index')

    elif request.method == 'GET':  # GET request
        invoice_form = InvoiceForm(instance=invoice)
        order_formset = OrderLineFormSet(
            instance=invoice, queryset=order_lines)

    context = {
        'invoice': invoice,
        'invoice_form': invoice_form,
        'order_formset': order_formset,

    }
    return render(request, 'invoices/form.html', context)


def save_invoice_pdf(request, inv_id):

    invoice = Invoice.objects.get(pk=inv_id)
    order_lines = OrderLine.objects.filter(invoice=invoice)

    context = {}
    context['invoice'] = invoice
    context['order_lines'] = order_lines
    context['empty_rows'] = range(16 - len(order_lines))

    pdf_render = WeasyTemplateResponse(
        request=request, template='invoices/invoice_pdf.html', context=context).rendered_content
    pdf_file_name = "{}-{}_{}_{}.pdf".format(
        invoice.sequence, invoice.number, invoice.customer.company.name.replace(" ", "-"), invoice.issued_date)

    # Overwrite existing pdf with the new one
    invoice.pdf_document.delete()
    invoice.pdf_document.save(pdf_file_name, ContentFile(pdf_render))

    return True


def check_pdf(request, id):
    invoice = Invoice.objects.get(pk=id)
    order_lines = OrderLine.objects.filter(invoice=invoice)

    context = {}
    context['invoice'] = invoice
    context['order_lines'] = order_lines
    context['empty_rows'] = range(16 - len(order_lines))

    return render(request, 'invoices/invoice_pdf.html', context)


def invoice_detail(request, id):
    invoice = Invoice.objects.get(pk=id)
    context = {}
    context['invoice'] = invoice

    return render(request, 'invoices/detail.html', context)


def send_invoices(invoices_list):
    GMAIL = env("GMAIL_ACCOUNT")
    GMAIL_PASSWORD = env("GMAIL_ACCOUNT_PWD")
    invoices_list = Invoice.objects.filter(
        id__in=invoices_list).order_by('customer')

    global_settings = GlobalSettings.objects.get_global_settings()

    customers = Customer.objects.all()

    invoices_queryset = None

    for customer in customers:
        invoices_queryset = Invoice.objects.filter(
            id__in=invoices_list).filter(customer=customer).values_list('sequence', 'number', 'pdf_document', 'mail_info')
        if not invoices_queryset:
            continue

        if send_invoice_email(GMAIL, GMAIL_PASSWORD, global_settings.issuer.company.name,
                              customer.company.contact.email, customer.company.contact.name, customer.company.contact.cc_email, invoices_queryset):
            for invoice in invoices_queryset:
                mail_info_id = invoice[3]
                MailInfo.objects.filter(
                    pk=mail_info_id).update(status="Delivered", sent_timestamp=datetime.now())
        else:
            for invoice in invoices_queryset:
                mail_info_id = invoice[3]
                MailInfo.objects.filter(
                    pk=mail_info_id).update(status="Failed")

    return HttpResponseRedirect('/')
