from django.shortcuts import render
from django import forms

from . import util

class SearchForm(forms.Form):
    q = forms.CharField(label="Search")

#Index view
def index(request):
    return render(request, "encyclopedia/index.html", {
         "form": SearchForm(),
         "entries": util.list_entries()
    })

#Search bar view
def search_entry(request):
    if request.method == "POST":
        
        form = SearchForm(request.POST)

        # Check if form data is valid (server-side)
        if form.is_valid():

            # Isolate the entry from the 'cleaned' version of form data
            query = form.cleaned_data["q"]
            
            print(query)
            #Retrieve all entries
            entries_list = util.list_entries()

            #Go through all entries and try to see if the query is in the list.
            for entry in entries_list:
                processed_entry = entry.split()[0].lower()
                if query.lower() in processed_entry:
                    entry = util.get_entry(query)
                    if entry is not None:
                        title = entry.split("#")[0]
                    else:
                        break
                    # Redirect user to list of entries
                    return render(request, "encyclopedia/read.html", {
                        "entry": entry,
                        "title": title,
                        "form": SearchForm()
                    })
            res = entries_list
            message = f"Entry for {query} may not exist. Please try a different search query."
            return render(request, "encyclopedia/search_results.html", {
                "entries": res,
                "message": message,
                "form": SearchForm()
            })
    else:
        res = util.list_entries()
        return render(request, "encyclopedia/search_result.html", {
            "form": SearchForm(),
            "entries": res
        })