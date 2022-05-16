from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.
def credit(request, invoice_uuid):
  messages.add_message(request, messages.ERROR, "Not implemented")
  return redirect("/")

def debit(request, invoice_uuid):
  messages.add_message(request, messages.ERROR, "Not implemented")
  return redirect("/")
