from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    # path('add_invoice/', views.add_invoice, name='add_invoice'),
    path('create_invoice/', views.create_invoice, name='create_invoice'),
    path('create_build_invoice/<int:id>/', views.create_build_invoice, name='create_build_invoice'),
    path('invoice_pdf/<int:id>/', views.invoice_pdf, name='invoice_pdf'),
    path('', views.index, name='index'),

    # ex: /polls/5/
    # path('<int:question_id>/', views.detail, name='detail'),
    # # ex: /polls/5/results/
    # path('<int:question_id>/results/', views.results, name='results'),
    # # ex: /polls/5/vote/
    # path('<int:question_id>/vote/', views.vote, name='vote'),
]
