import datetime
from typing import Any
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from .forms import ReserveBookForm
from .models import Book, Author, BookInstance




class AuthorCreateView(generic.CreateView):
    model = Author
    fields = "__all__"
    initial = {
        "date_of_death": "11/03/2009",
    }
    "http://localhost:63342/homework7.py/catalog/templates/create"


class AuthorUpdateView(generic.UpdateView):
    model = Author
    fields = ['name']
    "http://localhost:63342/homework7.py/catalog/templates/create"



class AuthorDeleteView(generic.DeleteView):
    model = Author
    success_url = reverse_lazy('author-list')
    "http://localhost:63342/homework7.py/catalog/templates/create"



class BookListView(generic.ListView):
    model = Book
    context_object_name = "book_list"
    queryset = Book.objects.all()
    template_name = "book/list.html"


def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    return super().get_context_data(**kwargs) | {"book_list": Book.objects.all()}


class BookDetailView(generic.DetailView):
    model = Book
    template_name = "book/detail.html"



VISITS_KEY = "visits"


def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact="a").count()
    num_authors = Author.objects.all().count()

    num_visits = request.seesion.get(VISITS_KEY, 0)
    request.session[VISITS_KEY] = num_visits + 1

    return render(
        request,
        "index.html",
        context={
            "num_books": num_books,
            "num_instances": num_instances,
            "num_instances_available": num_instances_available,
            "num_authors": num_authors,
            "num_visits": num_visits,
       },
    )


def reserve_book_form(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    if request.session == "POST":
        form = ReserveBookForm(request.POST)

        if form.is_valid():
            #  Perform action
           book_instance.status = "r"
           book_instance.due_back = form.cleaned_data("return_date")
           book_instance.save()

           # Redirect to success url
           return  HttpResponseRedirect("/")

    else:
        proposed_return_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = ReserveBookForm(initial={"return_date": proposed_return_date})

    return render(
        request,
        "book/reserve.html",
        {"form": form, "book_instance": book_instance},
    )