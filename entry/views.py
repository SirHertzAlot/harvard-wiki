import random

from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView, ListView
from .models import Entry
from django.db.models import Q

from encyclopedia import util

class NewEntryForm(forms.Form):
    title = forms.CharField(label="title")
    content = forms.CharField(label="content")

class EntryView(TemplateView):
    model = Entry
    template_name = 'encyclopedia/entry.html'

class SearchResultsView(ListView):
    model = Entry
    template_name = 'encyclopedia/search_results.html'

    def get_query(self):  # new
        return res

# Create your views here.

#Sub query entry

def subQuery(request):
    query = request.GET.get("q")
    query_list = util.list_entries()
    res = [i for i in query_list if query in i]
    entry = util.get_entry(res)
    if entry is not None:
        print(f"Received request from {request}")
        return render(request, "encyclopedia/entry.html", {
            "entry": entry
        })
    else:
        print(f"Received request from {request}")
        query_list = util.list_entries()
        return render(request, "encyclopedia/search_results.html", {
            "entries": entry
        } )
    
#Edit entry route
def edit_entry(request):
    if request.method == "POST":
        
        form = NewEntryForm(request.POST)

        # Check if form data is valid (server-side)
        if form.is_valid():

            # Isolate the entry from the 'cleaned' version of form data
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            # Add the new entry to our list of entries
            util.save_entry(title, content)

            # Redirect user to list of entries
            return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "encyclopedia/edit.html", {
            "form": NewEntryForm()
        })

# Create Entry view with form to send markdown entry to backend for validation & processing. 
def index(request):
    return render(request, "encyclopedia/create.html", {
        "form": NewEntryForm()
    })

# Random Entry view to send markdown entry to client for viewing. 
def random_entry(request):
    
    if request.method == "GET":
        entries = util.list_entries()
        entry = random.choice(entries)
        return render(request,"encyclopedia/read.html", {
            "entry": util.get_entry(entry)
        })
    else:
      # Redirect user to list of entries
        return HttpResponseRedirect(reverse("index"))

# Read Entry view to send markdown entry to client for viewing. 
def read_entry(request, title):

    if request.method == "GET":

        return render(request, "encyclopedia/read.html", {
            "entry": util.get_entry(title)
        })
    else:
      # Redirect user to list of entries
        return HttpResponseRedirect(reverse("index"))  

# Create Entry form validation & processing. 
def submit_entry(request):
    
    if request.method == 'POST':
        
        form = NewEntryForm(request.POST)

        # Check if form data is valid (server-side)
        if form.is_valid():

            # Isolate the entry from the 'cleaned' version of form data
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            # Add the new entry to our list of entries
            util.save_entry(title, content)

            # Redirect user to list of entries
            return HttpResponseRedirect(reverse("index"))

        else:

            # If the form is invalid, re-render the page with existing information.
            return render(request, "encyclopedia/create.html", {
                "form": form
            })