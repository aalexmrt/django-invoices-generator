from datetime import datetime

import environ
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django_weasyprint.views import WeasyTemplateResponse
from django.core.files.base import ContentFile
from invoices.forms import AddressForm, CompanyForm, ContactForm, InvoiceForm, OrderLineFormSet
from invoices.models import (
    Address,
    Company,
    Contact,
    Customer,
    GlobalSettings,
    Invoice,
    MailInfo,
    OrderLine,
    Product,
)
from invoices.utils.send_email import send_invoice_email
env = environ.Env()
env.read_env()


def view_invoices(request):
    invoices_list = Invoice.objects.order_by('-number')
    context = {
        'invoices_list': invoices_list
    }
    return render(request, 'invoices/view_invoices.html', context)


def add_invoice(request):

    new_invoice = Invoice.objects.create()
    new_invoice.save()
    print('from add_invoice', new_invoice.issuer)
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

            return redirect('view_invoices')

    elif request.method == 'GET':  # GET request
        invoice_form = InvoiceForm(instance=invoice)
        order_formset = OrderLineFormSet(
            instance=invoice, queryset=order_lines)

    context = {
        'invoice': invoice,
        'invoice_form': invoice_form,
        'order_formset': order_formset,

    }

    return render(request, 'invoices/form_invoice.html', context)


def delete_invoice(request, id):
    try:
        Invoice.objects.get(pk=id).delete()
    except:
        messages.error(request, 'Something went wrong')
        return redirect('view_invoices')

    return redirect('view_invoices')


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


def send_invoices(request):

    if request.method == 'POST':
        data = request.POST
        invoices_list = data.getlist('selected_options')
        GMAIL = env("GMAIL_ACCOUNT")
        GMAIL_PASSWORD = env("GMAIL_ACCOUNT_PWD")
        invoices_list = Invoice.objects.filter(
            id__in=invoices_list).order_by('customer')

        global_settings = GlobalSettings.objects.filter().first()

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


def add_customer(request):
    new_customer = Customer.objects.create()
    new_customer.save()
    return redirect('make_customer', new_customer.id)


def make_customer(request, id):
    # Get the customer object or return a 404 response if it doesn't exist
    customer = get_object_or_404(Customer, pk=id)
    print(request.POST)
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        address_form = AddressForm(request.POST)
        company_form = CompanyForm(request.POST)

        if contact_form.is_valid() and address_form.is_valid() and company_form.is_valid():

            if customer.company:  # Update existing company, contact, and address
                company = customer.company
                print(company_form.cleaned_data)
                company.name = company_form.cleaned_data['name']
                company.customer_information_file_number = company_form.cleaned_data[
                    'customer_information_file_number']
                company.contact.name = contact_form.cleaned_data['name']
                company.contact.email = contact_form.cleaned_data['email']
                company.contact.cc_email = contact_form.cleaned_data['cc_email']
                company.address.street = address_form.cleaned_data['street']
                company.address.city = address_form.cleaned_data['city']
                company.address.postal_code = address_form.cleaned_data['postal_code']

                company.contact.save()
                company.address.save()
                company.save()
            else:  # Create a new company if it doesn't exist
                contact = contact_form.save()
                address = address_form.save()
                company = Company.objects.create(
                    name=company_form.cleaned_data['name'],
                    customer_information_file_number=company_form.cleaned_data[
                        'customer_information_file_number'],
                    contact=contact,
                    address=address
                )
                customer.company = company
                customer.save()

            messages.success(request, 'Customer saved successfully')

            return redirect('view_customers')

    else:  # GET request
        contact_form = ContactForm(
            instance=customer.company.contact) if customer.company else ContactForm()
        address_form = AddressForm(
            instance=customer.company.address) if customer.company else AddressForm()
        company_form = CompanyForm(
            instance=customer.company) if customer.company else CompanyForm()

    context = {
        'contact_form': contact_form,
        'address_form': address_form,
        'company_form': company_form,
    }

    return render(request, 'invoices/form_customer.html', context)


def view_customers(request):
    customer_list = Customer.objects.order_by('company')
    context = {
        'customer_list': customer_list
    }
    return render(request, 'invoices/view_customers.html', context)


def delete_customer(request, id):
    try:
        customer = get_object_or_404(Customer, pk=id)
        if customer.company:
            company = customer.company
            company.address.delete()
            company.contact.delete()
            company.delete()
        customer.delete()
        messages.success(request, 'Customer deleted successfully')
    except Customer.DoesNotExist:
        messages.error(request, 'Customer not found')
    except Exception as e:
        messages.error(request, f'Something went wrong: {str(e)}')

    return redirect('view_customers')
