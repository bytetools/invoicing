from django.shortcuts import render
from invoices.models import Invoice

def index(request):
    return render(request, "core/index.html",
        {"invoices": Invoice.objects.all()}
    )
