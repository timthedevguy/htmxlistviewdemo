from django.shortcuts import render
from django.views.generic import TemplateView
from HTMXListViewDemo.views import HtmxListView
from hr_app.models import Person


# Create your views here.
class IndexView(TemplateView):
    template_name = "index.html"


class PersonListView(HtmxListView):
    paginate_by = 10
    model = Person
    template_name = "partials/_person_list.html"
    target_id = "#person-list"
    order_by = "name"
    queryset = Person.objects.all()